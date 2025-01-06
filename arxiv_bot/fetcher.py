import arxiv
from typing import List, Dict
from tqdm import tqdm
from .storage import PaperStorage
import time

class PaperFetcher:
    def __init__(self, ai_service, config):
        self.ai_service = ai_service
        self.config = config
        self.storage = PaperStorage()
        
    def fetch_papers(self, paper_type: str):
        total_start = time.time()
        
        type_config = self.config.get_paper_type_config(paper_type)
        general_config = self.config.get_general_config()
        
        print(f"\n📚 开始获取 {paper_type} 类型的论文...")
        print(f"🔍 搜索查询: {type_config['search_query']}")
        print(f"📋 目标论文数量: {type_config['max_papers']}\n")
        
        papers = []
        max_papers = type_config['max_papers']
        max_results_per_request = general_config['max_search_results']
        search_query = type_config['search_query']
        max_attempts = 3
        retry_delay = 5  # 重试等待时间（秒）
        
        search = arxiv.Search(
            query=search_query,
            max_results=general_config['max_search_results'] * max_attempts,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        results_iterator = iter(search.results())
        current_batch = 0

        while len(papers) < max_papers:
            try:
                print(f"\n📥 正在获取第 {current_batch + 1} 批论文")
                
                # 获取当前批次的论文
                current_papers = []
                for _ in range(max_results_per_request):
                    try:
                        current_papers.append(next(results_iterator))
                    except StopIteration:
                        print("\n📢 没有更多论文结果")
                        break
                
                if not current_papers:
                    break
                
                # 获取历史记录中最新的和最旧的论文ID
                latest_paper_id, oldest_paper_id = self.storage.get_latest_and_oldest_paper_id(paper_type)
                # 过滤已经推送过的论文
                if latest_paper_id:
                    current_papers = [r for r in current_papers if self._is_valid_paper(r.entry_id, latest_paper_id, oldest_paper_id)]
                
                relevant_count = 0
                for result in tqdm(current_papers, desc=f"🔍 正在分析论文相关性", unit="篇"):
                    if len(papers) >= max_papers:
                        break

                    if self.storage.is_paper_exists(paper_type, result.entry_id):
                        continue
                    
                    if self._is_relevant_paper(result.title, result.summary, type_config):
                        paper = {
                            'title': result.title,
                            'abstract': result.summary,
                            'url': result.entry_id
                        }
                        papers.append(paper)
                        self.storage.add_paper(paper_type, result.entry_id)
                        relevant_count += 1
                
                print(f"📊 其中相关论文: {relevant_count} 篇")
                current_batch += 1
            
            except Exception as e:
                print(f"\n❌ 发生错误: {str(e)}")
                time.sleep(retry_delay)
                continue
        
        total_time = time.time() - total_start
        print(f"\n✅ 论文获取完成!")
        print(f"⏱️ 总耗时: {total_time:.2f} 秒")
        print(f"📝 共获取相关论文: {len(papers)} 篇\n")
        
        return papers

        
    def _is_relevant_paper(self, title: str, abstract: str, type_config: Dict) -> bool:
        # 关键词检查
        for keyword in type_config['keywords']:
            if keyword in title.lower() or keyword in abstract.lower():
                return True
                
        # AI 相关性检查
        return self.ai_service.check_relevance(title, abstract, type_config['prompt']) 

    def _is_valid_paper(self, current_id: str, latest_id: str, oldest_id: str) -> bool:
        """
        比较两个论文ID，判断当前论文是否比最新的论文更新，并且比最旧的论文旧
        arxiv ID格式例如: 2403.12345v1
        """
        current_version = float(current_id.split('/')[-1].split('v')[0])
        latest_version = float(latest_id)
        oldest_version = float(oldest_id)
        return current_version > latest_version or current_version < oldest_version
import os
import arxiv
import requests
from datetime import datetime
import schedule
import time
from dotenv import load_dotenv
from typing import List, Dict
from tqdm import tqdm
import yaml

class ArxivPaperAgent:
    def __init__(self, config_path: str = "config.yaml"):
        load_dotenv()
        # 获取所有webhook URL
        self.webhook_urls = []
        i = 1
        while True:
            webhook_url = os.getenv(f'WEBHOOK_URL_{i}')
            if webhook_url:
                self.webhook_urls.append(webhook_url)
                i += 1
            else:
                break
                
        if not self.webhook_urls:
            raise ValueError("No webhook URLs found in environment variables")
            
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def is_relevant_paper(self, title: str, abstract: str, paper_type: str) -> bool:
        """根据配置判断论文是否相关"""
        type_config = self.config['paper_types'][paper_type]
        
        # 检查关键词
        for keyword in type_config['keywords']:
            if keyword in title.lower() or keyword in abstract.lower():
                return True
                
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = type_config['prompt'].format(title=title, abstract=abstract)
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.deepseek_url, headers=headers, json=data)
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content'].strip().lower()
                return "是" in answer
            return False
        except Exception as e:
            print(f"Error in relevance check: {e}")
            return False

    def fetch_papers(self, paper_type: str) -> List[Dict]:
        """获取指定类型的论文"""
        type_config = self.config['paper_types'][paper_type]
        search = arxiv.Search(
            query=type_config['search_query'],
            max_results=self.config['general']['max_search_results'],
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in tqdm(search.results(), desc=f"Fetching {paper_type} papers"):
            if self.is_relevant_paper(result.title, result.summary, paper_type):
                paper = {
                    'title': result.title,
                    'abstract': result.summary,
                    'url': result.entry_id
                }
                papers.append(paper)
                if len(papers) >= type_config['max_papers']:
                    break
        
        return papers

    def summarize_with_deepseek(self, abstract: str) -> str:
        """使用Deepseek API总结论文"""
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = self.config['general']['summary_prompt'].format(abstract=abstract)
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(self.deepseek_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return "Failed to generate summary."

    def send_to_feishu(self, summaries: List[Dict], paper_type: str):
        """发送消息到所有配置的飞书webhook"""
        type_config = self.config['paper_types'][paper_type]
        message = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{type_config['title']} - {datetime.now().strftime('%Y-%m-%d')}",
                        "content": [
                            [{
                                "tag": "text",
                                "text": f"📑 {paper['title']}\n"
                                       f"💡 总结: {paper['summary']}\n"
                                       f"🔗 链接: {paper['url']}\n\n"
                            }] for paper in summaries
                        ]
                    }
                }
            }
        }
        
        results = []
        for webhook_url in self.webhook_urls:
            try:
                response = requests.post(webhook_url, json=message)
                results.append(response.status_code == 200)
                print(f"Sent to webhook {webhook_url}: {'Success' if response.status_code == 200 else 'Failed'}")
            except Exception as e:
                print(f"Error sending to webhook {webhook_url}: {e}")
                results.append(False)
        
        return any(results)  # 只要有一个发送成功就返回True

    def run(self):
        """运行主流程"""
        for paper_type, config in self.config['paper_types'].items():
            if not config['enabled']:
                continue
                
            papers = self.fetch_papers(paper_type)
            if not papers:
                continue
                
            summaries = []
            for paper in papers:
                summary = self.summarize_with_deepseek(paper['abstract'])
                summaries.append({
                    'title': paper['title'],
                    'summary': summary,
                    'url': paper['url']
                })
            
            self.send_to_feishu(summaries, paper_type)

def main():
    agent = ArxivPaperAgent()
    # agent.run()
    schedule_time = agent.config['general']['schedule_time']
    schedule.every().day.at(schedule_time).do(agent.run)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
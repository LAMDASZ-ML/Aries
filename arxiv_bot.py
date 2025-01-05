import os
import arxiv
import requests
from datetime import datetime, timedelta
import schedule
import time
from dotenv import load_dotenv
from typing import List, Dict
import json
from tqdm import tqdm
# 加载环境变量
load_dotenv()

class ArxivPaperAgent:
    def __init__(self):
        self.webhook_url = os.getenv('WEBHOOK_URL')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
    
    def is_relevant_paper(self, title: str, abstract: str) -> bool:
        """使用Deepseek判断论文是否与LLM reasoning相关"""
        if 'reasoning' in title.lower() or 'reasoning' in abstract.lower():
            return True
        if 'fast and slow thinking' in title.lower() or 'fast and slow thinking' in abstract.lower():
            return True
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""请判断这篇论文是否与LLM推理(reasoning)、神经符号推理、逻辑推理、搜索、MCTS相关。
        
        标题: {title}
        摘要: {abstract}
        
        请只回答"是"或"否"。如果论文主要研究LLM的推理能力、推理方法、逻辑推理、神经符号推理、LLM search、Inference Scaling Law、Fast and Slow Thinking等主题，回答"是"；
        如果论文主要关注其他主题，回答"否"。"""
        
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

    def fetch_papers(self) -> List[Dict]:
        """获取最新的LLM相关论文并筛选"""
        # 设置搜索查询，获取更多论文以便筛选
        search = arxiv.Search(
            query="cat:cs.AI AND (LLM OR 'Large Language Model Reasoning' OR 'LLM Reasoning' OR 'Neuro-Symbolic' OR 'Fast and Slow Thinking')",
            max_results=100,  # 增加初始获取数量
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        # print([result.title for result in search.results()])
        papers = []
        for result in tqdm(search.results()):
            # 使用Deepseek判断论文相关性
            if self.is_relevant_paper(result.title, result.summary):
                paper = {
                    'title': result.title,
                    'abstract': result.summary,
                    'url': result.entry_id
                }
                papers.append(paper)
                # 当收集到足够的相关论文时停止
                if len(papers) >= 10:
                    break
        
        return papers

    def summarize_with_deepseek(self, abstract: str) -> str:
        """使用Deepseek API总结论文"""
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"请根据摘要用一句话总结这篇文章的核心内容: {abstract}"
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(self.deepseek_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return "Failed to generate summary."

    def send_to_feishu(self, summaries: List[Dict]):
        """发送消息到飞书"""
        message = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"今日LLM Reasoning论文更新 - {datetime.now().strftime('%Y-%m-%d')}",
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
        
        response = requests.post(self.webhook_url, json=message)
        return response.status_code == 200

    def run(self):
        """运行主流程"""
        papers = self.fetch_papers()
        summaries = []
        
        for paper in papers:
            summary = self.summarize_with_deepseek(paper['abstract'])
            summaries.append({
                'title': paper['title'],
                'summary': summary,
                'url': paper['url']
            })
        
        self.send_to_feishu(summaries)

def main():
    agent = ArxivPaperAgent()
    # agent.run()
    # 设置每天早上9点运行
    schedule.every().day.at("09:00").do(agent.run)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 
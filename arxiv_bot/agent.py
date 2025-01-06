from typing import List, Dict
from .config import Config
from .ai_service import AIService
from .fetcher import PaperFetcher
from .messenger import FeishuMessenger

class ArxivPaperAgent:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = Config(config_path)
        self.ai_service = AIService(self.config.api_key)
        self.fetcher = PaperFetcher(self.ai_service, self.config)
        self.messenger = FeishuMessenger(self.config.webhook_urls)
        
    def run(self):
        """运行主流程"""
        for paper_type, type_config in self.config.config['paper_types'].items():
            if not type_config['enabled']:
                continue
                
            papers = self.fetcher.fetch_papers(paper_type)
            if not papers:
                continue
                
            summaries = self._process_papers(papers)
            self.messenger.send_message(summaries, paper_type, type_config)
            
    def _process_papers(self, papers: List[Dict]) -> List[Dict]:
        summaries = []
        for paper in papers:
            summary = self.ai_service.summarize(
                paper['abstract'],
                self.config.get_general_config()['summary_prompt']
            )
            summaries.append({
                'title': paper['title'],
                'summary': summary,
                'url': paper['url']
            })
        return summaries 
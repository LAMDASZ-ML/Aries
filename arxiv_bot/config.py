from typing import Dict, Any
import os
import yaml
from dotenv import load_dotenv, dotenv_values

load_dotenv(override=True)

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self._load_config(config_path)
        self._load_env_vars()
        
    def _load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        for paper_type, details in self.config['paper_types'].items():
            if 'title' not in details:
                details['title'] = f"今日{paper_type}论文更新".upper()
            if 'prompt' not in details:
                details['prompt'] = self._generate_prompt(paper_type, details)
            if 'max_papers' not in details:
                details['max_papers'] = 5

        if 'summary_prompt' not in self.config['general']:
            self.config['general']['summary_prompt'] = "请根据摘要用一句话总结这篇文章的核心内容: {abstract}"

    def _generate_prompt(self, paper_type: str, details: Dict[str, Any]) -> str:
        """
        根据 paper_type 和 config.yaml 中的配置动态生成 prompt。
        """
        keywords = "、".join(details.get('keywords', []))
        search_query = details.get('search_query', '未定义搜索条件')
        
        prompt = (
            f"请反思批判性的判断这篇论文是否与以下主题相关：{keywords}。\n\n"
            f"标题: {{title}}\n"
            f"摘要: {{abstract}}\n\n"
            f"请只回答\"是\"或\"否\"。如果论文主要研究与以下关键词相关的主题：{keywords}，或符合搜索条件：{search_query}，回答\"是\"；\n"
            f"否者请回答\"否\"。"
        )
        return prompt
                
    def _load_env_vars(self):
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
            
        env_vars = dotenv_values('.env')
        self.api_key = env_vars.get('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
            
    def get_paper_type_config(self, paper_type: str) -> Dict[str, Any]:
        return self.config['paper_types'][paper_type]
        
    def get_general_config(self) -> Dict[str, Any]:
        return self.config['general'] 
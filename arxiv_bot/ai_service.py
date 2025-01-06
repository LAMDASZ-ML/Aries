import requests
from typing import Dict
import json

class AIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/chat/completions"
        
    def _call_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的学术论文助手，善于总结和分析论文内容。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                output = result['choices'][0]['message']['content']
                return output
            else:
                print(f"API response format error: {json.dumps(result, ensure_ascii=False)}")
                return ""
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""
            
    def check_relevance(self, title: str, abstract: str, prompt_template: str) -> bool:
        prompt = prompt_template.format(title=title, abstract=abstract)
        answer = self._call_api(prompt).strip().lower()
        return not ("否" in answer or "no" in answer)
        
    def summarize(self, abstract: str, prompt_template: str) -> str:
        prompt = prompt_template.format(abstract=abstract)
        result = self._call_api(prompt)
        if not result:
            return "抱歉，生成摘要时出现错误。"
        return result 
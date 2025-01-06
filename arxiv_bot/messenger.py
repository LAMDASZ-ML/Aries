import requests
from datetime import datetime
from typing import List, Dict

class FeishuMessenger:
    def __init__(self, webhook_urls: List[str]):
        self.webhook_urls = webhook_urls
        
    def send_message(self, summaries: List[Dict], paper_type: str, type_config: Dict) -> bool:
        message = self._format_message(summaries, paper_type, type_config)
        return self._send_to_webhooks(message)
        
    def _format_message(self, summaries: List[Dict], paper_type: str, type_config: Dict) -> Dict:
        return {
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
        
    def _send_to_webhooks(self, message: Dict) -> bool:
        results = []
        for webhook_url in self.webhook_urls:
            try:
                response = requests.post(webhook_url, json=message)
                success = response.status_code == 200
                results.append(success)
                print(f"Sent to webhook {webhook_url}: {'Success' if success else 'Failed'}")
            except Exception as e:
                print(f"Error sending to webhook {webhook_url}: {e}")
                results.append(False)
                
        return any(results) 
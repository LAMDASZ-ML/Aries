import json
import os
from typing import Set, Dict
from datetime import datetime

class PaperStorage:
    def __init__(self, storage_file: str = "paper_history.json"):
        self.storage_file = storage_file
        self.paper_history = self._load_history()
        
    def _load_history(self) -> Dict[str, Set[str]]:
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                history_dict = json.load(f)
                # 将列表转换为集合以提高查找效率
                return {k: set(v) for k, v in history_dict.items()}
        return {}
        
    def _save_history(self):
        # 将集合转换回列表以便JSON序列化
        history_dict = {k: list(v) for k, v in self.paper_history.items()}
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(history_dict, f, ensure_ascii=False, indent=2)
            
    def is_paper_exists(self, paper_type: str, paper_url: str) -> bool:
        return paper_url in self.paper_history.get(paper_type, set())
        
    def add_paper(self, paper_type: str, paper_url: str):
        if paper_type not in self.paper_history:
            self.paper_history[paper_type] = set()
        self.paper_history[paper_type].add(paper_url)
        self._save_history() 
        
    def get_latest_and_oldest_paper_id(self, paper_type: str) -> tuple:
        """
        获取指定类型中最新的和最旧的论文ID
        """
        papers = self.paper_history.get(paper_type, set())
        if not papers:
            return float('-inf'), float('inf') 
        
        try:
            paper_ids = []
            for pid in papers:
                id_part = pid.split('/')[-1].split('v')[0]
                paper_ids.append((pid, float(id_part)))
            
            latest = max(paper_ids, key=lambda x: x[1])
            oldest = min(paper_ids, key=lambda x: x[1])
            return latest[1], oldest[1]
        except:
            return float('-inf'), float('inf') 
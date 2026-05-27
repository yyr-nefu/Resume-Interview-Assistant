import json
import os
from typing import List, Dict, Any, Optional

class ArchiveManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def list_items(self, jd_id: Optional[str] = None) -> Dict[str, Any]:
        items = []
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    item_type = 'unknown'
                    if filename.startswith('jd_'):
                        item_type = 'jd'
                    elif filename.startswith('interview_'):
                        item_type = 'interview'
                    elif filename.startswith('note_'):
                        item_type = 'note'
                    elif filename.startswith('resume_'):
                        item_type = 'resume'
                    
                    item_jd_id = data.get('jd_id', '')
                    
                    if jd_id and item_jd_id != jd_id:
                        continue
                    
                    items.append({
                        'id': filename.replace('.json', ''),
                        'type': item_type,
                        'name': data.get('name', filename),
                        'created_at': data.get('created_at', ''),
                        'jd_id': item_jd_id
                    })
                except:
                    pass
        
        items.sort(key=lambda x: x['created_at'], reverse=True)
        
        return {'items': items}
        
    def get_item(self, item_id: str) -> Dict[str, Any]:
        file_path = os.path.join(self.data_dir, f"{item_id}.json")
        if not os.path.exists(file_path):
            raise ValueError("文件不存在")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
        
    def delete_item(self, item_id: str) -> Dict[str, Any]:
        file_path = os.path.join(self.data_dir, f"{item_id}.json")
        if not os.path.exists(file_path):
            raise ValueError("文件不存在")
        
        os.remove(file_path)
        return {'status': 'success', 'message': '删除成功'}
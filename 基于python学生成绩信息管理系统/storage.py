import json
import os

class DataStorage:
    def __init__(self, data_file="grade_data.json"):
        self.data_file = data_file

    def load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # 如果文件损坏或不存在，返回空数据
                return {}
        return {}

    def save(self, data):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存数据失败: {e}") 
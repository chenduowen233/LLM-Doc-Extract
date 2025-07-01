import os
import json
import yaml
from collections import defaultdict

class JSONCombiner:
    def __init__(self, config_path='config.yaml'):
        self.config = self._load_config(config_path)
        output_paths = self.config['extracting']['output_paths']
        self.voted_json_dir = output_paths['voted_json_dir']
        self.combined_json_dir = output_paths['combined_json_dir']

    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def combine_jsons(self):
        os.makedirs(self.combined_json_dir, exist_ok=True)
        
        # 按基础名称分组文件（例如：cloudflare_01.json -> cloudflare）
        file_groups = defaultdict(list)
        for filename in os.listdir(self.voted_json_dir):
            if filename.endswith('.json'):
                parts = filename.rsplit('_', 1)
                if len(parts) > 1 and parts[1].replace('.json', '').isdigit():
                    base_name = parts[0]
                else:
                    base_name = filename.replace('.json', '')
                file_groups[base_name].append(os.path.join(self.voted_json_dir, filename))
        
        for base_name, file_paths in file_groups.items():
            combined_data = {}
            for file_path in sorted(file_paths):  # 按文件名排序以确保顺序一致
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        combined_data.update(data)
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                combined_data.update(item)
            
            output_path = os.path.join(self.combined_json_dir, f"{base_name}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=4)
            print(f"已将 {len(file_paths)} 个文件合并到 {output_path}")

if __name__ == '__main__':
    combiner = JSONCombiner()
    combiner.combine_jsons()
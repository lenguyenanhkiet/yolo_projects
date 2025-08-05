import os
import yaml
from config import DATA_DIR

def create_data_yaml(class_map: dict):
    class_names = [None] * len(class_map)
    for name, idx in class_map.items():
        class_names[idx] = name

    data_yaml = {
        'names': class_names,
        'nc': len(class_names),
        'path': str(DATA_DIR),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test'
    }

    yaml_path = os.path.join(DATA_DIR, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data_yaml, f, default_flow_style=False, allow_unicode=True)

    print("✅ Đã tạo xong data.yaml với các class sau:")
    for i, name in enumerate(class_names):
        print(f"  {i}: {name}")

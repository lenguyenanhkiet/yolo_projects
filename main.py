from extract_and_prepare import get_class_map
from create_yaml import create_data_yaml
# from train_yolo import train_and_eval
# from predict_test import predict_test

if __name__ == "__main__":
    class_map = get_class_map()
    create_data_yaml(class_map)
    for i, name in class_map.items():
        print(f"  {i}: {name}")
    # train_and_eval()
    # predict_test()

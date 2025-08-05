from src.update_and_split import update_dataset_and_split
from src.create_yaml import create_data_yaml
from src.train_yolo import train_and_eval
from src.predict_test import predict_test
from src.export_to_tflite import export_to_tflite

if __name__ == "__main__":
    class_map = update_dataset_and_split()
    create_data_yaml(class_map)
    for name, index in class_map.items():
        print(f"{index}: {name}")

    train_and_eval()
    # predict_test()
    export_to_tflite()

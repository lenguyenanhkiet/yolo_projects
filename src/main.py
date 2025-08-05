from src.update_and_split import update_dataset_and_split
from src.create_yaml import create_data_yaml
from src.train_yolo import train_and_eval
from src.predict_test import predict_test
from src.export_to_tflite import export_to_tflite

if __name__ == "__main__":
    # Bước 1: Cập nhật dataset (lọc trùng, chia train/val/test, đổi tên, cập nhật nhãn)
    class_map = update_dataset_and_split()

    # Bước 2: Tạo file data.yaml cho YOLO
    create_data_yaml(class_map)

    # Bước 3: Huấn luyện
    train_and_eval()

    # Bước 4: Dự đoán
    # predict_test()

    # Bước 5: Xuất sang TFLite
    # export_to_tflite()

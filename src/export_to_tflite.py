import os
from ultralytics import YOLO

def export_to_tflite():
    model_path = "runs/train/result_train/weights/best.pt"
    # Kiểm tra file .pt có tồn tại không
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"❌ Không tìm thấy mô hình: {model_path}")

    # Nạp mô hình và export
    model = YOLO(model_path)
    result = model.export(format="tflite")  # Mặc định lưu cùng thư mục

    # Hiển thị thông tin mô hình xuất
    if result is not None:
        print(f"✅ Export thành công: {result}")
    else:
        print("❌ Export thất bại.")

from config import OUTPUT_DIR, MODEL_CONFIG, EPOCHS, IMG_SIZE, BATCH, DEVICE, PROJECT_NAME
from ultralytics import YOLO
import shutil
from pathlib import Path
def train_and_eval():
    model = YOLO(MODEL_CONFIG)
    yaml_path = OUTPUT_DIR / 'data.yaml'
    shutil.rmtree("runs/train/result_train", ignore_errors=True)
    model.train(
        data=str(yaml_path),
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH,
        name="result_train",  # tên cụ thể của lần train
        project="runs/train",  # nơi lưu project (ví dụ: 'data/')
        exist_ok=True,
        device=DEVICE
    )
    best_weight = Path("runs/train/result_train/weights/best.pt")
    metrics = model.val(
        data=str(yaml_path),
        imgsz=IMG_SIZE,
        batch=BATCH,
        split='test',
        device=DEVICE
    )

    with open("runs/train/result_train/result_map.txt", "w") as f:
        f.write(f"mAP50: {metrics.box.map50:.4f}\n")
        f.write(f"mAP50-95: {metrics.box.map:.4f}\n")

    print(f"✅ mAP50: {metrics.box.map50:.4f}, mAP50-95: {metrics.box.map:.4f}")

from config import IMAGE_DIR, IMG_SIZE, DEVICE
from ultralytics import YOLO

def predict_test():
    model = YOLO("runs/detect/result_train/weights/best.pt")
    model.predict(
        source=str(IMAGE_DIR / 'test'),
        imgsz=IMG_SIZE,
        save=True,
        name='result_test',
        conf=0.25,
        device=DEVICE
    )

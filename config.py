from pathlib import Path

DATA_DIR = Path("data")

ROOT_DIR = Path("data")
RAW_DIR = ROOT_DIR / "raw"
IMAGE_DIR = ROOT_DIR / "images"
LABEL_DIR = ROOT_DIR / "labels"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

OUTPUT_DIR = ROOT_DIR  # hoặc bạn có thể dùng Path("runs/train")
MODEL_CONFIG = "yolov8n.yaml"
EPOCHS = 10
IMG_SIZE = 640
BATCH = 16
DEVICE = "cpu"
PROJECT_NAME = "yolo_train"

# update_and_split.py
import os
import json
import uuid
import random
import shutil
import hashlib
from pathlib import Path
from config import RAW_DIR, IMAGE_DIR, LABEL_DIR, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, OUTPUT_DIR

HASH_LOG_PATH = OUTPUT_DIR / "hash_log.json"

def get_file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def update_dataset_and_split():
    # Load hoặc khởi tạo hash log
    if HASH_LOG_PATH.exists():
        with open(HASH_LOG_PATH, "r") as f:
            hash_log = json.load(f)
    else:
        hash_log = {}

    # Lấy danh sách class từ thư mục con của raw/
    class_names = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(RAW_DIR / d)])
    class_to_index = {name: idx for idx, name in enumerate(class_names)}
    print("📦 Danh sách class phát hiện:", class_to_index)

    # Tạo thư mục output nếu chưa có
    for split in ["train", "val", "test"]:
        (IMAGE_DIR / split).mkdir(parents=True, exist_ok=True)
        (LABEL_DIR / split).mkdir(parents=True, exist_ok=True)

    new_data = []

    # Quét ảnh mới từ raw/
    for class_name in class_names:
        class_dir = RAW_DIR / class_name
        img_files = [f for f in os.listdir(class_dir) if f.lower().endswith((".jpg", ".png"))]

        for img_file in img_files:
            img_path = class_dir / img_file
            base = os.path.splitext(img_file)[0]
            label_path = class_dir / f"{base}.txt"

            file_hash = get_file_hash(img_path)
            if file_hash in hash_log:
                continue  # Bỏ qua nếu đã tồn tại

            unique_id = uuid.uuid4().hex[:8]
            new_base = f"{class_name}_{unique_id}"

            new_data.append((img_path, label_path, class_name, new_base, file_hash))

    print(f"🔍 Phát hiện {len(new_data)} ảnh mới cần thêm vào dataset.")

    # Shuffle và chia tỉ lệ
    random.shuffle(new_data)
    total = len(new_data)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)
    splits = {
        "train": new_data[:train_end],
        "val": new_data[train_end:val_end],
        "test": new_data[val_end:],
    }

    for split, items in splits.items():
        for img_path, label_path, class_name, new_base, file_hash in items:
            class_idx = class_to_index[class_name]
            dst_img = IMAGE_DIR / split / f"{new_base}.jpg"
            dst_lbl = LABEL_DIR / split / f"{new_base}.txt"

            shutil.copy2(img_path, dst_img)

            if label_path.exists():
                with open(label_path, "r") as f:
                    lines = f.readlines()

                new_lines = []
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        parts[0] = str(class_idx)
                        new_lines.append(" ".join(parts))

                with open(dst_lbl, "w") as f:
                    f.write("\n".join(new_lines))

            hash_log[file_hash] = {
                "class": class_name,
                "new_name": new_base,
                "split": split,
            }

    # Ghi lại hash_log
    with open(HASH_LOG_PATH, "w") as f:
        json.dump(hash_log, f, indent=2)

    print("✅ Đã cập nhật dataset và chia train/val/test hợp lý.")

    return class_to_index

import os
import shutil
import random
import hashlib
import uuid
from pathlib import Path
from tqdm import tqdm
from config import RAW_DIR, IMAGE_DIR, LABEL_DIR, TRAIN_RATIO, VAL_RATIO, TEST_RATIO

def hash_img(img_path):
    with open(img_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def prepare_dataset(class_map: dict):
    print("🚧 Bắt đầu xử lý dữ liệu: lọc trùng, gán nhãn, chia train/val/test...")

    # Tạo thư mục đích
    for split in ['train', 'val', 'test']:
        (IMAGE_DIR / split).mkdir(parents=True, exist_ok=True)
        (LABEL_DIR / split).mkdir(parents=True, exist_ok=True)

    all_data = []
    seen_hashes = set()

    for class_name, class_idx in class_map.items():
        class_folder = RAW_DIR / class_name
        if not class_folder.exists():
            print(f"⚠️ Bỏ qua: Không tìm thấy thư mục {class_folder}")
            continue

        all_images = list(class_folder.glob("*.jpg"))

        for img_path in tqdm(all_images, desc=f"📂 {class_name}"):
            img_hash = hash_img(img_path)
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)

            label_path = img_path.with_suffix(".txt")
            if not label_path.exists():
                continue

            all_data.append((img_path, label_path, class_idx, class_name))

    print(f"📊 Tổng số ảnh sau lọc trùng: {len(all_data)}")

    # Shuffle và chia dữ liệu
    random.shuffle(all_data)
    total = len(all_data)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    split_map = {
        'train': all_data[:train_end],
        'val': all_data[train_end:val_end],
        'test': all_data[val_end:]
    }

    for split, data in split_map.items():
        for img_path, label_path, class_idx, class_name in data:
            unique_id = uuid.uuid4().hex[:8]
            new_name = f"{class_name}_{unique_id}"

            dst_img = IMAGE_DIR / split / f"{new_name}.jpg"
            dst_lbl = LABEL_DIR / split / f"{new_name}.txt"

            shutil.copy2(img_path, dst_img)

            # Ghi file nhãn mới
            with open(label_path, 'r') as f:
                lines = list(set(f.readlines()))

            with open(dst_lbl, 'w') as f:
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        parts[0] = str(class_idx)  # Cập nhật class ID
                        f.write(" ".join(parts) + "\n")

    print("✅ Hoàn tất chuẩn bị dữ liệu. Tạo xong ảnh và nhãn trong thư mục train/val/test.")


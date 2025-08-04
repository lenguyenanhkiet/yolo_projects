import os
import shutil
import hashlib
import uuid
from pathlib import Path
from config import RAW_DIR, IMAGE_DIR, LABEL_DIR, TRAIN_RATIO, VAL_RATIO, TEST_RATIO

# === Phát hiện class ===
CLASS_NAMES = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))])
CLASS_TO_INDEX = {name: idx for idx, name in enumerate(CLASS_NAMES)}

def get_class_map():
    return CLASS_TO_INDEX

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

print("📦 Danh sách class phát hiện:", CLASS_TO_INDEX)

# === Tạo folder đích ===
for split in ['train', 'val', 'test']:
    (IMAGE_DIR / split).mkdir(parents=True, exist_ok=True)
    (LABEL_DIR / split).mkdir(parents=True, exist_ok=True)
print("📁 Đã tạo (nếu chưa có) các thư mục: train, val, test.")

# === Ghi nhật ký hash để lọc trùng ===
seen_hashes = set()
duplicate_count = 0
all_data = []

# === Xử lý từng class ===
for class_name in CLASS_NAMES:
    class_dir = RAW_DIR / class_name
    img_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.png'))]

    for img_file in img_files:
        base_name = os.path.splitext(img_file)[0]
        src_img_path = class_dir / img_file
        src_txt_path = class_dir / f"{base_name}.txt"

        file_hash = get_file_hash(src_img_path)
        if file_hash in seen_hashes:
            duplicate_count += 1
            continue
        seen_hashes.add(file_hash)

        unique_id = uuid.uuid4().hex[:8]
        new_base = f"{class_name}_{unique_id}"

        all_data.append((src_img_path, src_txt_path, class_name, new_base))

print(f"🔍 Tổng số ảnh sau lọc trùng: {len(all_data)} (Bỏ qua {duplicate_count} ảnh trùng lặp)")

# === Chia train/val/test theo tỉ lệ ===
import random
random.shuffle(all_data)
total = len(all_data)
train_end = int(total * TRAIN_RATIO)
val_end = train_end + int(total * VAL_RATIO)

splits = {
    'train': all_data[:train_end],
    'val': all_data[train_end:val_end],
    'test': all_data[val_end:]
}

for split, items in splits.items():
    for img_path, txt_path, class_name, new_base in items:
        class_idx = CLASS_TO_INDEX[class_name]
        dst_img = IMAGE_DIR / split / f"{new_base}.jpg"
        dst_lbl = LABEL_DIR / split / f"{new_base}.txt"

        shutil.copy2(img_path, dst_img)

        if txt_path.exists():
            with open(txt_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    parts[0] = str(class_idx)
                    new_lines.append(" ".join(parts))

            with open(dst_lbl, 'w') as f:
                f.write("\n".join(new_lines))

print("✅ Đã đổi tên ảnh bằng UUID theo class, cập nhật nhãn, lọc ảnh trùng, chia dữ liệu vào train/val/test.")

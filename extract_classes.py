import os
import shutil
import hashlib

RAW_DIR = 'data/raw'
CLASS_NAMES = sorted([d for d in os.listdir(RAW_DIR) if os.path.isdir(os.path.join(RAW_DIR, d))])
CLASS_TO_INDEX = {name: idx for idx, name in enumerate(CLASS_NAMES)}

def get_class_map():
    return CLASS_TO_INDEX

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

print("📦 Danh sách class phát hiện:", CLASS_TO_INDEX)

# OUTPUT_IMG_DIR = 'data/images'
# OUTPUT_LABEL_DIR = 'data/labels'
#
# os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
# os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)
#
# # Để lưu trữ hash của ảnh đã xử lý
# seen_hashes = set()
# duplicate_count = 0
#
# for class_name in CLASS_NAMES:
#     class_dir = os.path.join(RAW_DIR, class_name)
#     img_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.png'))]
#
#     for img_file in img_files:
#         base_name = os.path.splitext(img_file)[0]
#         src_img_path = os.path.join(class_dir, img_file)
#         src_txt_path = os.path.join(class_dir, base_name + '.txt')
#
#         file_hash = get_file_hash(src_img_path)
#         if file_hash in seen_hashes:
#             duplicate_count += 1
#             continue  # Bỏ qua ảnh trùng
#         seen_hashes.add(file_hash)
#
#         # Tên mới: <class>_<tên>.jpg
#         new_name = f"{class_name}_{base_name}"
#         new_img_path = os.path.join(OUTPUT_IMG_DIR, new_name + '.jpg')
#         new_txt_path = os.path.join(OUTPUT_LABEL_DIR, new_name + '.txt')
#
#         shutil.copy(src_img_path, new_img_path)
#
#         if os.path.exists(src_txt_path):
#             with open(src_txt_path, 'r') as f:
#                 lines = f.readlines()
#
#             new_lines = []
#             for line in lines:
#                 parts = line.strip().split()
#                 if len(parts) == 5:
#                     parts[0] = str(CLASS_TO_INDEX[class_name])
#                     new_lines.append(' '.join(parts))
#
#             with open(new_txt_path, 'w') as f:
#                 f.write('\n'.join(new_lines))
#
# print(f"✅ Đã copy ảnh và ghi nhãn lại theo class index. Đã bỏ qua {duplicate_count} ảnh trùng lặp.")

import os
import shutil

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
MAX_IMAGES = 200

def reduce_dataset(input_folder, output_folder='reduced_dataset'):
    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' not found.")
        return

    os.makedirs(output_folder, exist_ok=True)

    class_folders = [f for f in os.listdir(input_folder)
                     if os.path.isdir(os.path.join(input_folder, f))]

    for class_name in class_folders:
        src_class_path = os.path.join(input_folder, class_name)
        dst_class_path = os.path.join(output_folder, class_name)
        os.makedirs(dst_class_path, exist_ok=True)

        # Filter only image files
        images = [f for f in os.listdir(src_class_path)
                  if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]

        images = images[:MAX_IMAGES]

        for img_file in images:
            shutil.copy(
                os.path.join(src_class_path, img_file),
                os.path.join(dst_class_path, img_file)
            )

        print(f"  {class_name}: copied {len(images)} images")

    print(f"\nDone. Reduced dataset saved to '{output_folder}'")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python reduce_dataset.py <input_dataset_folder>")
        print("Example: python reduce_dataset.py dataset/train")
    else:
        reduce_dataset(sys.argv[1])

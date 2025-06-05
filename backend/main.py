import os
from optimiser import compress_image


def is_image_file(filename: str) -> bool:
    return filename.lower().endswith(('png', 'jpeg', 'jpg', 'webp'))


def process_file(input_path: str, output_path: str, max_width: int, quality: int, to_format: str):
    with open(input_path, "rb") as f:
        image_bytes = f.read()
        
    optimized = compress_image(image_bytes, max_width=max_width, quality=quality, to_format=to_format)

    os.makedirs(output_path, exist_ok = True)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_path, f"{base_name}.{to_format}")
    
    with open(output_path, "wb") as out_file:
        out_file.write(optimized)


def process_image_or_directory(input_path: str, output_dir: str, max_width: int, quality: int, to_format: str):
    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if is_image_file(file):
                    input_file_path = os.path.join(root, file)
                    rel_path = os.path.realpath(input_file_path, input_path)
                    output_file_path = os.path.join(
                        output_dir, os.path.splitext(rel_path)[0] + f".{to_format.lower()}"
                    )
                    print(f"Optimizing: {input_file_path} -> {output_file_path}")
                    process_file(input_file_path, output_file_path, max_width, quality, to_format)
    else:
        if os.path.isdir(output_dir):
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_file_path = os.path.join(output_dir, base_name + f"{to_format.lower()}")
        else:
            output_file_path = output_dir                    

        print(f"Optimizing : {input_path} -> {output_file_path}")    
        process_file(input_file_path, output_file_path, max_width, quality, to_format)
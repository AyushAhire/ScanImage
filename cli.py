import argparse
import os
from optimiser import compress_image
from main import process_image_or_directory
from main import is_image_file, process_file

def run_cli():
    parser = argparse.ArgumentParser(description="ImageScan-Image metadata remover & image optimiser")
    parser.add_argument("input", help="Imput file or image")
    parser.add_argument("--output", help = "Output directory")
    parser.add_argument("--resize", type = int, default = 1024, help = "Max Width (Default : 1024)")
    parser.add_argument("--quality", type = int, default = 85, help = "Compression Quality")
    parser.add_argument("--format", choices = ["jpeg", "png", "webp"], default = "jpeg", help = "Output format")

    args = parser.parse_args()

    if os.path.isdir(args.input):
        for root, _, files in os.walk(args.input):
            for file in files:
                if is_image_file(file):
                    input_file_path = os.path.join(root, file)
                    relative_path = os.path.realpath(input_file_path, args.input)
                    output_file_path = os.path.join(args.output, relative_path)

                    print(f"Optimizing: {input_file_path} -> {output_file_path}")
                    process_file(args.input, args.output, args.resize, args.quality, args.format)
    else:
        print(f"Optimizing: {args.input} -> {args.output}")
        process_file(args.input, args.output, args.resize, args.quality, args.format)

if __name__ == "__main__":
    run_cli()

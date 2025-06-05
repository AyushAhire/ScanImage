from PIL import Image
from io import BytesIO
import io

def strip_metadata(image: Image.Image) -> Image.Image:
    size = (int(image.size[0]), int(image.size[1]))
    new_img = Image.new(image.mode, size)
    new_img.putdata(list(image.getdata()))
    return new_img

def compress_image(image_bytes: bytes, max_width: int = 1024, quality: int=85, to_format: str = 'JPEG') -> BytesIO:
    img = Image.open(BytesIO(image_bytes))
    
    #strip metadata
    img = strip_metadata(img)

    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    out_buffer = BytesIO()
    save_params = {"optimise": True, "quality": quality}

    if to_format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    img.save(out_buffer, format = to_format, **save_params)
    out_buffer.seek(0)
    output = io.BytesIO()
    img.save(output, format=to_format.upper(), quality=quality)
    return output.getvalue()
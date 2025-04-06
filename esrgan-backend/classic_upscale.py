import io
from PIL import Image, ImageFilter

# Bicubic Interpolation: smooth upscaling 
def upscale_bicubic(image_bytes, scale=4):
    # Load image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Image resize
    width, height = img.size
    new_size = (width * scale, height * scale)
    upscaled_img = img.resize(new_size, Image.BICUBIC)
    return image_to_bytes(upscaled_img)

# Lanczos Resampling: high-quality upscaling (Preverse edges)
def upscale_lanczos(image_bytes, scale=4):
    # Load image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Image resize
    width, height = img.size
    new_size = (width * scale, height * scale)
    upscaled_img = img.resize(new_size, Image.LANCZOS)
    return image_to_bytes(upscaled_img)

# Unsharp Mask: sharpen the image after upscaling (Combine with Bicubic)
def upscale_bicubic_sharpen(image_bytes, scale=4):
    # Load image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    # Image resize
    width, height = img.size
    new_size = (width * scale, height * scale)
    upscaled_img = img.resize(new_size, Image.BICUBIC)
    # Apply unsharp mask filter
    sharpened_img = upscaled_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    return image_to_bytes(sharpened_img)


def image_to_bytes(pil_image, format="PNG"):
    buffer = io.BytesIO()
    pil_image.save(buffer, format=format)
    return buffer.getvalue()
from __future__ import annotations

from PIL import Image, ImageEnhance



def enhance_for_preview(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    image = ImageEnhance.Sharpness(image).enhance(1.05)
    image = ImageEnhance.Contrast(image).enhance(1.03)
    return image

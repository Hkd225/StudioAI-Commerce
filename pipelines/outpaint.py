from __future__ import annotations

from PIL import Image, ImageFilter

from core.utils import ensure_rgb
from pipelines.inpaint import run_inpainting



def prepare_outpainting(image: Image.Image, expand_pixels: int = 128) -> tuple[Image.Image, Image.Image]:
    image = ensure_rgb(image)
    w, h = image.size
    new_w = max(64, w + expand_pixels * 2)
    new_h = max(64, h + expand_pixels * 2)
    new_w -= new_w % 8
    new_h -= new_h % 8

    bg = image.resize((new_w, new_h), resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(radius=30))
    canvas = bg.copy()
    paste_x = (new_w - w) // 2
    paste_y = (new_h - h) // 2
    canvas.paste(image, (paste_x, paste_y))

    mask = Image.new("L", (new_w, new_h), 255)
    keep = Image.new("L", (w, h), 0)
    mask.paste(keep, (paste_x, paste_y))
    return canvas, mask



def run_outpainting(models: dict, image: Image.Image, prompt: str, expand_pixels: int = 128, seed: int = 42):
    canvas, mask = prepare_outpainting(image, expand_pixels=expand_pixels)
    return run_inpainting(models, canvas, mask, prompt=prompt, strength=1.0, seed=seed)

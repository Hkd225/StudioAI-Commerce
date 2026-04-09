from __future__ import annotations

from PIL import Image

from pipelines.automask import simple_foreground_mask
from pipelines.inpaint import run_inpainting
from pipelines.outpaint import run_outpainting



def auto_mask(image: Image.Image) -> Image.Image:
    return simple_foreground_mask(image)



def replace_background(models: dict, image: Image.Image, prompt: str, seed: int = 42) -> Image.Image:
    mask = auto_mask(image)
    inverted_mask = mask.point(lambda x: 255 - x)
    return run_inpainting(models, image, inverted_mask, prompt=prompt, strength=0.98, seed=seed)



def edit_with_mask(models: dict, image: Image.Image, mask: Image.Image, prompt: str, strength: float, seed: int = 42) -> Image.Image:
    return run_inpainting(models, image, mask, prompt=prompt, strength=strength, seed=seed)



def expand_canvas(models: dict, image: Image.Image, prompt: str, expand_pixels: int, seed: int = 42) -> Image.Image:
    return run_outpainting(models, image, prompt=prompt, expand_pixels=expand_pixels, seed=seed)

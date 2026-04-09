from __future__ import annotations

import random
from textwrap import fill

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from core.scheduler import set_scheduler



def _mock_image(prompt: str, seed: int, width: int = 768, height: int = 768) -> Image.Image:
    rng = random.Random(seed)
    base = np.zeros((height, width, 3), dtype=np.uint8)
    c1 = np.array([rng.randint(20, 180), rng.randint(20, 180), rng.randint(120, 240)], dtype=np.uint8)
    c2 = np.array([rng.randint(120, 255), rng.randint(20, 180), rng.randint(20, 180)], dtype=np.uint8)
    for y in range(height):
        alpha = y / max(height - 1, 1)
        base[y, :, :] = ((1 - alpha) * c1 + alpha * c2).astype(np.uint8)
    image = Image.fromarray(base, mode="RGB")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, 40, width - 40, height - 40), radius=28, outline="white", width=4)
    font = ImageFont.load_default()
    draw.text((56, 56), "MOCK MODE", fill="white", font=font)
    wrapped = fill(prompt[:220], width=34)
    draw.multiline_text((56, 100), wrapped, fill="white", font=font, spacing=6)
    for i in range(8):
        x0 = rng.randint(80, width - 200)
        y0 = rng.randint(200, height - 200)
        x1 = x0 + rng.randint(40, 180)
        y1 = y0 + rng.randint(40, 180)
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, outline=(255, 255, 255), width=2)
    return image



def generate_images(models: dict, prompt: str, negative_prompt: str, seed: int, steps: int, cfg: float, num_images: int = 1, scheduler_name: str = "Euler A") -> list[Image.Image]:
    pipe = models.get("txt2img")
    if pipe is None:
        return [_mock_image(prompt, seed + i) for i in range(num_images)]

    pipe = set_scheduler(pipe, scheduler_name)
    import torch
    device = pipe.device.type if hasattr(pipe, "device") else "cpu"
    generators = [torch.Generator(device=device).manual_seed(int(seed) + i) for i in range(int(num_images))]

    result = pipe(
        prompt=[prompt] * int(num_images),
        negative_prompt=[negative_prompt] * int(num_images),
        generator=generators,
        num_inference_steps=int(steps),
        guidance_scale=float(cfg),
        num_images_per_prompt=1,
    )
    return result.images

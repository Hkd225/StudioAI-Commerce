from __future__ import annotations

from pipelines.postprocess import enhance_for_preview
from pipelines.txt2img import generate_images



def generate_batch(models: dict, prompt: str, negative_prompt: str, seed: int, steps: int, cfg: float, num_images: int, scheduler_name: str):
    images = generate_images(models, prompt, negative_prompt, seed, steps, cfg, num_images, scheduler_name)
    return [enhance_for_preview(img) for img in images]

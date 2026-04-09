"""Compatibility layer untuk notebook lama."""
from __future__ import annotations

from core.memory import flush_memory
from core.model_loader import load_models
from pipelines.inpaint import run_inpainting
from pipelines.outpaint import prepare_outpainting
from services.generate_service import generate_batch



def load_models_cached():
    models = load_models()
    return models.get("txt2img"), models.get("inpaint")



def generate_image(pipe, prompt, neg_prompt, seed, steps, cfg, num_images=1, scheduler_name="Euler A"):
    models = {"txt2img": pipe, "inpaint": None}
    return generate_batch(models, prompt, neg_prompt, seed, steps, cfg, num_images, scheduler_name)

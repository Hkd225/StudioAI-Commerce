from __future__ import annotations

from functools import lru_cache

from core.config import Settings, get_settings


@lru_cache(maxsize=1)
def load_models() -> dict:
    settings = get_settings()
    if settings.mock_mode:
        return {"txt2img": None, "inpaint": None, "runtime": "mock"}

    try:
        import torch
        from diffusers import StableDiffusionInpaintPipeline, StableDiffusionPipeline
    except Exception as exc:
        return {"txt2img": None, "inpaint": None, "runtime": f"mock (missing deps: {exc})"}

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    txt2img = StableDiffusionPipeline.from_pretrained(
        settings.model_id,
        torch_dtype=dtype,
        safety_checker=None,
        use_auth_token=settings.hf_token,
    ).to(device)
    inpaint = StableDiffusionInpaintPipeline.from_pretrained(
        settings.inpaint_model_id,
        torch_dtype=dtype,
        safety_checker=None,
        use_auth_token=settings.hf_token,
    ).to(device)

    txt2img.enable_attention_slicing()
    inpaint.enable_attention_slicing()
    return {"txt2img": txt2img, "inpaint": inpaint, "runtime": device}

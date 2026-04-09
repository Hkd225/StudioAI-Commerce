from __future__ import annotations

from PIL import Image, ImageChops, ImageDraw, ImageFont

from core.utils import ensure_mask, ensure_rgb



def _mock_inpaint(image: Image.Image, mask: Image.Image, prompt: str) -> Image.Image:
    image = ensure_rgb(image).copy()
    mask = ensure_mask(mask, image.size)
    overlay = Image.new("RGB", image.size, (99, 102, 241))
    blended = Image.blend(image, overlay, 0.35)
    result = Image.composite(blended, image, mask)
    draw = ImageDraw.Draw(result)
    draw.text((20, 20), f"INPAINT: {prompt[:50]}", fill="white", font=ImageFont.load_default())
    return result



def run_inpainting(models: dict, image: Image.Image, mask: Image.Image, prompt: str, strength: float = 0.85, negative_prompt: str = "", steps: int = 35, cfg: float = 8.5, seed: int = 42):
    image = ensure_rgb(image)
    mask = ensure_mask(mask, image.size)
    pipe = models.get("inpaint")

    if pipe is None:
        return _mock_inpaint(image, mask, prompt)

    import torch
    device = pipe.device.type if hasattr(pipe, "device") else "cpu"
    generator = torch.Generator(device=device).manual_seed(int(seed))
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=image,
        mask_image=mask,
        strength=float(strength),
        guidance_scale=float(cfg),
        num_inference_steps=int(steps),
        generator=generator,
    )
    return result.images[0]

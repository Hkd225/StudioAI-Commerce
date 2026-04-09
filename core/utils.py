from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "studioai-output"



def ensure_rgb(image: Image.Image) -> Image.Image:
    return image.convert("RGB") if image.mode != "RGB" else image



def ensure_mask(mask: Image.Image, size: tuple[int, int]) -> Image.Image:
    if mask.mode != "L":
        mask = mask.convert("L")
    if mask.size != size:
        mask = mask.resize(size, resample=Image.NEAREST)
    return mask



def pil_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()



def make_side_by_side(left: Image.Image, right: Image.Image, label_left: str = "Before", label_right: str = "After") -> Image.Image:
    left = ensure_rgb(left)
    right = ensure_rgb(right)
    width = max(left.width, right.width)
    left = ImageOps.contain(left, (width, left.height))
    right = ImageOps.contain(right, (width, right.height))

    header_h = 48
    canvas = Image.new("RGB", (left.width + right.width, max(left.height, right.height) + header_h), "white")
    canvas.paste(left, (0, header_h))
    canvas.paste(right, (left.width, header_h))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, left.width, header_h), fill="#f3f4f6")
    draw.rectangle((left.width, 0, left.width + right.width, header_h), fill="#ede9fe")
    font = ImageFont.load_default()
    draw.text((12, 16), label_left, fill="black", font=font)
    draw.text((left.width + 12, 16), label_right, fill="black", font=font)
    return canvas



def list_saved_images(folder: Path | str) -> list[Path]:
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS])



def corner_background_color(image: Image.Image) -> np.ndarray:
    image = ensure_rgb(image)
    arr = np.asarray(image, dtype=np.float32)
    patches = [
        arr[:10, :10],
        arr[:10, -10:],
        arr[-10:, :10],
        arr[-10:, -10:],
    ]
    return np.concatenate([p.reshape(-1, 3) for p in patches], axis=0).mean(axis=0)

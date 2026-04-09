from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter

from core.utils import corner_background_color, ensure_rgb



def simple_foreground_mask(image: Image.Image) -> Image.Image:
    image = ensure_rgb(image)
    arr = np.asarray(image, dtype=np.float32)
    bg = corner_background_color(image)
    dist = np.linalg.norm(arr - bg, axis=2)
    threshold = max(22.0, float(np.percentile(dist, 65)))
    mask = (dist > threshold).astype(np.uint8) * 255
    pil_mask = Image.fromarray(mask, mode="L")
    pil_mask = pil_mask.filter(ImageFilter.MedianFilter(size=5))
    pil_mask = pil_mask.filter(ImageFilter.MaxFilter(size=7))
    pil_mask = pil_mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    return pil_mask.point(lambda x: 255 if x > 60 else 0)

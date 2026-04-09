from __future__ import annotations

import io
import zipfile
from datetime import datetime
from pathlib import Path

from PIL import Image

from core.utils import pil_to_bytes, slugify


def save_image(image: Image.Image, folder: str | Path, prefix: str = "result") -> Path:
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(prefix)}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
    path = folder / filename
    image.save(path)
    return path


def build_export_zip(entries: list[dict], readme_text: str | None = None) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        if readme_text:
            zf.writestr("README_EXPORT.txt", readme_text)
        for idx, entry in enumerate(entries, start=1):
            image = entry["image"]
            label = slugify(entry.get("label") or f"image-{idx}")
            zf.writestr(f"images/{idx:02d}-{label}.png", pil_to_bytes(image))
            meta = {k: v for k, v in entry.items() if k != "image"}
            meta_lines = [f"{k}: {v}" for k, v in meta.items()]
            zf.writestr(f"images/{idx:02d}-{label}.txt", "\n".join(meta_lines))
    return buffer.getvalue()

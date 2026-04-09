from __future__ import annotations

import streamlit as st
from PIL import Image

from core.utils import pil_to_bytes



def render_header(runtime: str) -> None:
    st.title("🛍️ StudioAI Commerce")
    st.caption("AI Product Photo Studio untuk UMKM dan marketplace.")
    st.info(f"Runtime aktif: {runtime}. Aktifkan MOCK_MODE=0 untuk memakai model Diffusers sungguhan.")



def download_image_button(image: Image.Image, label: str, file_name: str) -> None:
    st.download_button(label, data=pil_to_bytes(image), file_name=file_name, mime="image/png", use_container_width=True)

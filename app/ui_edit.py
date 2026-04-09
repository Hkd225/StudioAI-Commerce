from __future__ import annotations

import numpy as np
import streamlit as st
from PIL import Image, ImageFilter

from app.components import download_image_button
from core.utils import ensure_mask, make_side_by_side
from services.edit_service import auto_mask, edit_with_mask, expand_canvas, replace_background
from services.preset_service import BACKGROUND_PRESETS

try:
    from streamlit_drawable_canvas import st_canvas
except Exception:  # pragma: no cover
    st_canvas = None



def _get_source_image(state: dict):
    uploaded = st.session_state.get("uploaded_image")
    return uploaded or state.get("current_image")



def render_edit_tab(models: dict, state: dict) -> None:
    st.subheader("Edit Produk")
    uploaded = st.file_uploader("Upload foto produk", type=["png", "jpg", "jpeg", "webp"])
    if uploaded is not None:
        st.session_state["uploaded_image"] = Image.open(uploaded).convert("RGB")
        state["current_image"] = st.session_state["uploaded_image"]

    source_img = _get_source_image(state)
    if source_img is None:
        st.info("Upload foto produk atau pilih hasil generate dulu.")
        return

    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        st.image(source_img, caption="Gambar aktif", use_container_width=True)
        if st.button("Auto-mask produk", use_container_width=True):
            state["current_mask"] = auto_mask(source_img)
            st.success("Mask berhasil dibuat.")
        if state.get("current_mask") is not None:
            st.image(state["current_mask"], caption="Mask aktif", use_container_width=True)

    with col_b:
        mode = st.radio("Mode", ["Background Replacement", "Manual Inpainting", "Outpainting"], horizontal=True)

        if mode == "Background Replacement":
            preset = st.selectbox("Preset", list(BACKGROUND_PRESETS.keys()))
            custom = st.text_area("Prompt background", value=BACKGROUND_PRESETS[preset], height=100)
            seed = st.number_input("Seed edit", min_value=0, value=42, step=1, key="bg_seed")
            if st.button("Ganti background", type="primary", use_container_width=True):
                result = replace_background(models, source_img, custom, seed=int(seed))
                state["current_image"] = result
                state["history"].append({"label": "background-replacement", "prompt": custom, "kind": "background", "image": result})
                st.image(make_side_by_side(source_img, result), caption="Before / After", use_container_width=True)
                download_image_button(result, "Download hasil", "studioai-background.png")

        elif mode == "Manual Inpainting":
            prompt = st.text_input("Prompt edit", value="add premium cosmetic props and clean reflections")
            strength = st.slider("Strength", 0.1, 1.0, 0.85)
            seed = st.number_input("Seed inpaint", min_value=0, value=42, step=1, key="inpaint_seed")
            if st_canvas is None:
                st.warning("streamlit-drawable-canvas belum terpasang. Fitur manual mask tidak aktif.")
            else:
                canvas = st_canvas(
                    fill_color="rgba(255, 255, 255, 1.0)",
                    stroke_width=18,
                    stroke_color="#ffffff",
                    background_image=source_img,
                    update_streamlit=True,
                    height=source_img.height,
                    width=source_img.width,
                    drawing_mode="freedraw",
                    key="studioai_canvas",
                )
                if st.button("Jalankan inpainting", type="primary", use_container_width=True):
                    if canvas.image_data is None:
                        st.warning("Belum ada coretan mask.")
                    else:
                        mask_data = canvas.image_data[:, :, 3]
                        mask_data[mask_data > 0] = 255
                        mask = Image.fromarray(mask_data.astype("uint8"), mode="L")
                        mask = ensure_mask(mask, source_img.size).filter(ImageFilter.MaxFilter(15))
                        result = edit_with_mask(models, source_img, mask, prompt, float(strength), seed=int(seed))
                        state["current_image"] = result
                        state["current_mask"] = mask
                        state["history"].append({"label": "manual-inpaint", "prompt": prompt, "kind": "inpaint", "image": result})
                        st.image(make_side_by_side(source_img, result), caption="Before / After", use_container_width=True)
                        download_image_button(result, "Download hasil", "studioai-inpaint.png")

        elif mode == "Outpainting":
            prompt = st.text_area("Prompt outpaint", value="wider commercial product shot, detailed background, clean composition", height=100)
            expand_pixels = st.slider("Expand pixels", 64, 256, 128, step=16)
            seed = st.number_input("Seed outpaint", min_value=0, value=42, step=1, key="outpaint_seed")
            if st.button("Perluas kanvas", type="primary", use_container_width=True):
                result = expand_canvas(models, source_img, prompt, expand_pixels=int(expand_pixels), seed=int(seed))
                state["current_image"] = result
                state["history"].append({"label": "outpaint", "prompt": prompt, "kind": "outpaint", "image": result})
                st.image(make_side_by_side(source_img, result), caption="Before / After", use_container_width=True)
                download_image_button(result, "Download hasil", "studioai-outpaint.png")

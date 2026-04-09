from __future__ import annotations

import streamlit as st

from app.components import download_image_button
from services.generate_service import generate_batch
from services.preset_service import BACKGROUND_PRESETS, PRODUCT_PROMPTS



def render_generate_tab(models: dict, state: dict) -> None:
    left, right = st.columns([1, 1], gap="large")
    with left:
        st.subheader("Generate Product Scene")
        product_type = st.selectbox("Kategori produk", list(PRODUCT_PROMPTS.keys()))
        bg_style = st.selectbox("Preset background", ["Custom"] + list(BACKGROUND_PRESETS.keys()))
        base_prompt = PRODUCT_PROMPTS[product_type]
        bg_prompt = "" if bg_style == "Custom" else BACKGROUND_PRESETS[bg_style]
        prompt = st.text_area("Prompt", value=f"{base_prompt}, {bg_prompt}".strip(", "), height=140)
        negative_prompt = st.text_input("Negative prompt", value="blurry, distorted, low quality, text watermark")
        steps = st.slider("Steps", 10, 50, 30)
        cfg = st.slider("CFG", 1.0, 20.0, 7.5)
        seed = st.number_input("Seed", min_value=0, value=42, step=1)
        num_images = st.slider("Batch size", 1, 4, 2)
        scheduler_name = st.selectbox("Scheduler", ["Euler A", "DPM++", "DDIM"])
        if st.button("Generate", type="primary", use_container_width=True):
            images = generate_batch(models, prompt, negative_prompt, int(seed), steps, float(cfg), int(num_images), scheduler_name)
            state["generated_images"] = images
            state["current_image"] = images[0] if images else None
            for idx, image in enumerate(images, start=1):
                state["history"].append({"label": f"generate-{idx}", "prompt": prompt, "kind": "generate", "image": image})
            st.success(f"Berhasil membuat {len(images)} gambar.")

    with right:
        st.subheader("Hasil")
        if state.get("generated_images"):
            cols = st.columns(2)
            for idx, image in enumerate(state["generated_images"]):
                with cols[idx % 2]:
                    st.image(image, caption=f"Varian {idx+1}", use_container_width=True)
                    if st.button(f"Pilih varian {idx+1}", key=f"select_gen_{idx}", use_container_width=True):
                        state["current_image"] = image
                    download_image_button(image, "Download PNG", f"studioai-generate-{idx+1}.png")
        else:
            st.info("Belum ada gambar. Isi prompt lalu tekan Generate.")

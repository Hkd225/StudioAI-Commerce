from __future__ import annotations

import streamlit as st

from app.components import render_header
from app.ui_edit import render_edit_tab
from app.ui_generate import render_generate_tab
from app.ui_history import render_history_tab
from core.config import ensure_dirs, get_settings
from core.memory import flush_memory
from core.model_loader import load_models



def _init_state() -> dict:
    st.session_state.setdefault("generated_images", [])
    st.session_state.setdefault("current_image", None)
    st.session_state.setdefault("current_mask", None)
    st.session_state.setdefault("history", [])
    return st.session_state



def render_app() -> None:
    st.set_page_config(page_title="StudioAI Commerce", page_icon="🛍️", layout="wide")
    settings = get_settings()
    ensure_dirs(settings)
    state = _init_state()
    models = load_models()

    render_header(models.get("runtime", "unknown"))
    with st.sidebar:
        st.header("Kontrol Sistem")
        st.write("Project ini disusun dari notebook submission dan blueprint markdown yang kamu upload.")
        if st.button("Flush memory", use_container_width=True):
            flush_memory()
            st.success("Memory dibersihkan.")
        st.code("streamlit run app.py", language="bash")

    tab_generate, tab_edit, tab_history = st.tabs(["Generate", "Edit", "History"])
    with tab_generate:
        render_generate_tab(models, state)
    with tab_edit:
        render_edit_tab(models, state)
    with tab_history:
        render_history_tab(state)


if __name__ == "__main__":
    render_app()

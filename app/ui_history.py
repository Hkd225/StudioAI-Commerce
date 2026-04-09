from __future__ import annotations

import streamlit as st

from services.export_service import build_export_zip



def render_history_tab(state: dict) -> None:
    st.subheader("Riwayat & Export")
    history = state.get("history", [])
    if not history:
        st.info("Belum ada riwayat hasil.")
        return

    for idx, item in enumerate(reversed(history), start=1):
        with st.expander(f"{idx}. {item.get('kind', 'result')} - {item.get('label', 'image')}"):
            st.write({k: v for k, v in item.items() if k != 'image'})
            st.image(item['image'], use_container_width=True)

    zip_bytes = build_export_zip(history, readme_text="Export dari StudioAI Commerce")
    st.download_button(
        "Download semua hasil (ZIP)",
        data=zip_bytes,
        file_name="studioai-session-export.zip",
        mime="application/zip",
        use_container_width=True,
    )

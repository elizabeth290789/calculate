from pathlib import Path

import streamlit as st


def apply_base_styles() -> None:
    """Inject shared styles from a dedicated stylesheet."""
    css_path = Path(__file__).resolve().parent.parent / "styles.css"
    css_content = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

import streamlit as st

from utils.home import render_home_page
from utils.ui import apply_base_styles


st.set_page_config(
    page_title="A/B Test Toolkit",
    page_icon="📊",
    layout="wide",
)

apply_base_styles()
render_home_page()

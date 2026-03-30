import streamlit as st


def apply_base_styles() -> None:
    """Inject shared, low-risk visual improvements for all pages."""
    st.markdown(
        """
        <style>
        :root {
            --bg: #f7f9fc;
            --surface: #ffffff;
            --text: #111827;
            --muted: #6b7280;
            --border: #e5e7eb;
            --primary: #1d4ed8;
            --shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            --radius: 16px;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .block-container {
            padding-top: 2.25rem;
            padding-bottom: 2.5rem;
            max-width: 1100px;
        }

        h1, h2, h3 {
            letter-spacing: -0.015em;
        }

        [data-testid="stSidebar"] {
            background: #fbfcff;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #374151;
        }

        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
        }

        .stButton > button {
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

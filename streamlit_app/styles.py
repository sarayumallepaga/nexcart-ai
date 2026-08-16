import streamlit as st


def load_styles():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background: #FAF7F2;
            color: #242321;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 4rem;
            max-width: 1250px;
        }

        .nexcart-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 30px;
            font-weight: 800;
            color: #242321;
            letter-spacing: -1.5px;
        }

        .nexcart-logo span {
            color: #B85C38;
        }

        .nexcart-tagline {
            color: #77736C;
            font-size: 13px;
            margin-top: -5px;
        }

        .hero {
            padding: 55px 20px 45px 20px;
            text-align: center;
        }

        .hero-eyebrow {
            color: #B85C38;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
        }

        .hero-title {
            font-family: 'Outfit', sans-serif;
            font-size: 48px;
            font-weight: 700;
            letter-spacing: -2px;
            line-height: 1.05;
            color: #242321;
            margin: 0;
        }

        .hero-title span {
            color: #B85C38;
        }

        .hero-description {
            max-width: 650px;
            margin: 18px auto 0 auto;
            color: #77736C;
            font-size: 17px;
            line-height: 1.6;
        }

        .search-label {
            font-size: 13px;
            font-weight: 600;
            color: #77736C;
            margin-bottom: 6px;
        }

        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #242321;
            margin-top: 35px;
            margin-bottom: 5px;
        }

        .section-subtitle {
            color: #77736C;
            font-size: 14px;
            margin-bottom: 20px;
        }

        .product-card {
            background: #FFFFFF;
            border: 1px solid #E8E1D8;
            border-radius: 20px;
            padding: 18px;
            height: 100%;
        }

        .ai-card {
            background: #FFFDFC;
            border: 1px solid #E8E1D8;
            border-left: 4px solid #B85C38;
            border-radius: 18px;
            padding: 22px;
        }

        .ai-card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 19px;
            font-weight: 700;
            color: #242321;
        }

        .ai-card-text {
            color: #625E58;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 8px;
        }

        .stButton > button {
            border-radius: 12px;
            border: 1px solid #D8D0C6;
            background: #FFFFFF;
            color: #242321;
            font-weight: 600;
        }

        .stButton > button:hover {
            border-color: #B85C38;
            color: #B85C38;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
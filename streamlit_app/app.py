import streamlit as st

from styles import load_styles
from api import (
    login_user,
    get_all_products,
    shopping_chat,
)
from components import product_card


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NexCart — Shop Smarter",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_styles()


# ==========================================
# SESSION STATE
# ==========================================

if "token" not in st.session_state:
    st.session_state.token = None


# ==========================================
# LOGIN
# ==========================================

if not st.session_state.token:

    st.title("NexCart")

    st.caption(
        "AI-powered shopping intelligence"
    )

    st.divider()

    st.header("Welcome back")

    st.write(
        "Sign in to continue shopping smarter."
    )

    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
        )

        submitted = st.form_submit_button(
            "Sign In",
            width="stretch",
        )

        if submitted:

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                try:

                    data = login_user(
                        email,
                        password,
                    )

                    st.session_state.token = (
                        data["access_token"]
                    )

                    st.rerun()

                except Exception as error:

                    st.error(str(error))

    st.stop()


# ==========================================
# HEADER
# ==========================================

top_left, top_right = st.columns(
    [6, 2]
)


with top_left:

    st.title("NexCart")

    st.caption(
        "AI-powered shopping intelligence"
    )


with top_right:

    if st.button(
        "Logout",
        width="stretch",
    ):

        st.session_state.token = None

        st.rerun()


st.divider()


# ==========================================
# HERO
# ==========================================

st.caption(
    "AI SHOPPING ASSISTANT"
)

st.header(
    "Shop smarter. Buy with confidence."
)

st.write(
    "NexCart compares products, understands "
    "customer reviews, predicts prices and "
    "helps you make better buying decisions."
)


# ==========================================
# SEARCH
# ==========================================

search = st.text_input(
    "What are you looking for?",
    placeholder=(
        "Try: best phone under ₹50,000..."
    ),
)


# ==========================================
# AI SHOPPING ASSISTANT
# ==========================================

st.divider()

st.subheader(
    "✦ Ask NexCart AI"
)

st.caption(
    "Tell NexCart what you are looking for "
    "and get personalized shopping advice."
)

chat_query = st.text_input(
    "What do you want to know?",
    placeholder=(
        "Try: Which phone should I buy under ₹70,000?"
    ),
    key="shopping_chat_input",
)


if st.button(
    "Ask NexCart AI",
    width="stretch",
):

    if not chat_query.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        with st.spinner(
            "NexCart AI is thinking..."
        ):

            try:

                chat_result = shopping_chat(
                    chat_query
                )

                ai_response = chat_result.get(
                    "response",
                    "Sorry, I couldn't generate a response.",
                )

                st.markdown(
                    "### ✦ NexCart AI"
                )

                st.info(
                    ai_response
                )

            except Exception as error:

                st.error(
                    f"AI assistant unavailable: {error}"
                )


# ==========================================
# CATEGORIES
# ==========================================

st.subheader(
    "Explore categories"
)

st.caption(
    "Find products that match what you need."
)

categories = [
    "All",
    "Phones",
    "Laptops",
    "Audio",
    "Tablets",
    "TVs",
    "Home",
    "Gaming",
]


category_cols = st.columns(
    len(categories)
)


for col, category in zip(
    category_cols,
    categories,
):

    with col:

        st.button(
            category,
            width="stretch",
        )


# ==========================================
# AI FEATURES
# ==========================================

st.subheader(
    "What NexCart can do"
)

st.caption(
    "Your personal AI shopping intelligence."
)


feature_cols = st.columns(4)


features = [
    (
        "✦",
        "AI Buy Advice",
        "Know whether a product is actually worth buying.",
    ),
    (
        "◈",
        "Review Intelligence",
        "Turn hundreds of reviews into useful insights.",
    ),
    (
        "↗",
        "Price Prediction",
        "Know whether you should buy now or wait.",
    ),
    (
        "⌁",
        "Better Alternatives",
        "Discover products that may suit you better.",
    ),
]


for col, feature in zip(
    feature_cols,
    features,
):

    icon, title, description = feature

    with col:

        st.markdown(
            f"### {icon}"
        )

        st.write(
            f"**{title}**"
        )

        st.caption(
            description
        )


# ==========================================
# WHY NEXCART
# ==========================================

st.subheader(
    "Why NexCart?"
)

st.caption(
    "Stop spending hours researching before every purchase."
)


benefit_cols = st.columns(3)


benefits = [
    (
        "01",
        "Compare",
        "See products and their important differences in one place.",
    ),
    (
        "02",
        "Understand",
        "Let AI turn thousands of reviews into simple insights.",
    ),
    (
        "03",
        "Decide",
        "Get a clear recommendation based on value, price and your needs.",
    ),
]


for col, benefit in zip(
    benefit_cols,
    benefits,
):

    number, title, description = benefit

    with col:

        st.markdown(
            f"### {number}"
        )

        st.write(
            f"**{title}**"
        )

        st.caption(
            description
        )


# ==========================================
# PRODUCTS
# ==========================================

st.subheader(
    "Featured products"
)

st.caption(
    "Explore products from our catalog."
)


try:

    products = get_all_products(
        st.session_state.token
    )

    if products:

        product_cols = st.columns(3)

        for index, product in enumerate(
            products
        ):

            with product_cols[
                index % 3
            ]:

                product_card(product)

    else:

        st.info(
            "No products found."
        )


except Exception as error:

    st.error(
        f"Unable to load products: {error}"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "NexCart · AI-powered shopping intelligence"
)
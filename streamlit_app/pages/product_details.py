
import streamlit as st

from styles import load_styles
from api import (
    get_product_by_id,
    get_buy_advice,
    get_review_summary,
    get_price_prediction,
    get_alternatives,
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NexCart — Product Details",
    page_icon="🛒",
    layout="wide",
)

load_styles()


# ==========================================
# AUTH CHECK
# ==========================================

if "token" not in st.session_state:
    st.session_state.token = None

if not st.session_state.token:

    st.warning(
        "Please login from the NexCart home page."
    )

    st.stop()


# ==========================================
# GET SELECTED PRODUCT
# ==========================================

if "selected_product_id" not in st.session_state:

    st.error("No product selected.")

    if st.button("← Go to Home"):
        st.switch_page("app.py")

    st.stop()


product_id = st.session_state.selected_product_id

# ==========================================
# GET PRODUCT
# ==========================================

try:

    product = get_product_by_id(
        product_id,
        st.session_state.token,
    )

    if not product:

        st.error("Product not found.")

        if st.button("← Go to Home"):
            st.switch_page("app.py")

        st.stop()

except Exception as error:

    st.error(
        f"Unable to load product: {error}"
    )

    if st.button("← Go to Home"):
        st.switch_page("app.py")

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
    "← Back to Products",
    use_container_width=True,
):

    st.session_state.selected_product_id = None
    st.switch_page("app.py")


st.divider()


# ==========================================
# PRODUCT INFORMATION
# ==========================================

st.caption(
    f"{product.get('brand', '')} · "
    f"{product.get('store', '')}"
)

st.title(product["name"])


left, right = st.columns(
    [1, 1]
)


# ------------------------------------------
# Left: Product
# ------------------------------------------
with left:

    image_url = product.get("image")

    if image_url:

        st.image(
            image_url,
            width="stretch",
        )

    else:

        st.markdown("## 🛍️")

        st.caption(
            "Product image unavailable."
        )
        
# ------------------------------------------
# Right: Information
# ------------------------------------------

with right:

    st.subheader(
        product["name"]
    )

    st.markdown(
        f"## ₹{product['price']:,.0f}"
    )

    st.write(
        f"⭐ {product.get('rating', 0)}"
    )

    st.write(
        f"Available at: "
        f"{product.get('store', 'N/A')}"
    )

    st.write(
        product.get(
            "description",
            "No description available.",
        )
    )

    st.info(
        f"Warranty: "
        f"{product.get('warranty', 'N/A')}"
    )


# ==========================================
# AI BUY ADVICE
# ==========================================

st.divider()

st.subheader("✦ NexCart AI Advice")

try:

    advice_data = get_buy_advice(
        product_id
    )

    advice = advice_data.get(
        "advice",
        "No advice available.",
    )

    st.info(advice)

except Exception as error:

    st.warning(
        f"AI advice unavailable: {error}"
    )


# ==========================================
# REVIEW INTELLIGENCE
# ==========================================

st.divider()

st.subheader("✦ Review Intelligence")

try:

    review_data = get_review_summary(
        product_id
    )

    summary = review_data.get(
        "summary",
        "No review summary available.",
    )

    st.info(summary)

except Exception as error:

    st.warning(
        f"Review summary unavailable: {error}"
    )


# ==========================================
# PRICE PREDICTION
# ==========================================

st.divider()

st.subheader("↗ Price Prediction")

try:

    prediction_data = get_price_prediction(
        product_id
    )

    prediction = prediction_data.get(
        "prediction",
        "No price prediction available.",
    )

    st.info(prediction)

except Exception as error:

    st.warning(
        f"Price prediction unavailable: {error}"
    )


# ==========================================
# SPECIFICATIONS
# ==========================================

st.divider()

st.subheader("Specifications")

specifications = product.get(
    "specifications",
    {},
)

if specifications:

    for key, value in specifications.items():

        st.write(
            f"**{key}:** {value}"
        )

else:

    st.caption(
        "No specifications available."
    )


# ==========================================
# BETTER ALTERNATIVES
# ==========================================

st.divider()

st.subheader("⌁ Better Alternatives")

st.caption(
    "AI-powered alternatives that may offer better value."
)

try:

    alternatives_data = get_alternatives(
        product_id
    )

    alternatives = alternatives_data.get(
        "alternatives",
        [],
    )

    # Handle nested backend response
    if isinstance(alternatives, dict):

        alternatives = alternatives.get(
            "alternatives",
            [],
        )

    if alternatives:

        # If AI returns product IDs, fetch their
        # complete product information.
        alternative_products = []

        for alternative in alternatives:

            # If backend returns a product ID
            if isinstance(alternative, str):

                try:

                    alt_product = get_product_by_id(
                        alternative,
                        st.session_state.token,
                    )

                    if alt_product:
                        alternative_products.append(
                            alt_product
                        )

                except Exception:
                    pass

            # If backend already returns product objects
            elif isinstance(alternative, dict):

                alternative_products.append(
                    alternative
                )

        if alternative_products:

            alternative_cols = st.columns(
                min(3, len(alternative_products))
            )

            for index, alternative in enumerate(
                alternative_products
            ):

                with alternative_cols[
                    index % len(alternative_cols)
                ]:

                    with st.container(border=True):

                        # ------------------------------
                        # IMAGE
                        # ------------------------------

                        image_url = alternative.get(
                            "image"
                        )

                        if image_url:

                            st.image(
                                image_url,
                                width=180,
                            )

                        else:

                            st.markdown(
                                """
                                <div style="
                                    height:150px;
                                    display:flex;
                                    align-items:center;
                                    justify-content:center;
                                    font-size:50px;
                                ">
                                    🛍️
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        # ------------------------------
                        # PRODUCT INFO
                        # ------------------------------

                        st.write(
                            f"**{alternative.get('name', 'Unknown Product')}**"
                        )

                        st.caption(
                            alternative.get(
                                "brand",
                                "",
                            )
                        )

                        st.markdown(
                            f"### ₹{alternative.get('price', 0):,.0f}"
                        )

                        st.write(
                            f"⭐ {alternative.get('rating', 0)}"
                        )

                        # ------------------------------
                        # VIEW PRODUCT
                        # ------------------------------

                        if st.button(
                            "View Product",
                            key=(
                                f"alternative_"
                                f"{alternative.get('id', index)}"
                            ),
                            width="stretch",
                        ):

                            st.session_state.selected_product_id = (
                                alternative.get("id")
                            )

                            st.switch_page(
                                "pages/product_details.py"
                            )

        else:

            # Backend may currently be returning
            # product names instead of IDs.
            st.info(
                "AI found alternatives, but product "
                "details are not available yet."
            )

    else:

        st.info(
            "No better alternatives found."
        )

except Exception as error:

    st.warning(
        f"Alternatives unavailable: {error}"
    )

# ==========================================
# CUSTOMER REVIEWS
# ==========================================

st.divider()

st.subheader("Customer Reviews")

reviews = product.get(
    "reviews",
    [],
)

if reviews:

    for review in reviews:

        st.write(
            f"💬 {review}"
        )

else:

    st.caption(
        "No reviews available."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "NexCart · AI-powered shopping intelligence"
)
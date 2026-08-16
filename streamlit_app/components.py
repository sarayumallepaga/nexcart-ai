import streamlit as st


def product_card(product):

    name = product.get("name", "Unknown Product")
    brand = product.get("brand", "")
    price = product.get("price", 0)
    rating = product.get("rating", 0)
    store = product.get("store", "")

    product_id = product.get("id")

    with st.container(border=True):

        # ======================================
        # PRODUCT IMAGE
        # ======================================

        image_url = product.get("image", "")

        if image_url:

            st.image(
                image_url,
                width=180,
            )

        else:

            st.markdown(
                """
                <div style="
                    text-align:center;
                    font-size:60px;
                    padding:20px;
                ">
                    🛍️
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ======================================
        # PRODUCT INFO
        # ======================================

        st.caption(brand)

        st.subheader(name)

        st.markdown(
            f"### ₹{price:,.0f}"
        )

        st.write(
            f"⭐ {rating}  ·  {store}"
        )

        # ======================================
        # VIEW PRODUCT
        # ======================================

        if st.button(
            "View Product",
            key=f"view_{product_id}",
            width="stretch",
        ):

            # Save selected product
            st.session_state.selected_product_id = product_id

            # Navigate to separate product page
            st.switch_page(
                "pages/product_details.py"
            )
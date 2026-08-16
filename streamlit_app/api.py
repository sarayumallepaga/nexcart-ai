import requests


API_URL = "http://127.0.0.1:8000"


def login_user(email, password):
    response = requests.post(
        f"{API_URL}/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    if not response.ok:
        try:
            data = response.json()
            message = data.get("detail", "Login failed")
        except Exception:
            message = "Login failed"

        raise Exception(message)

    return response.json()


def get_all_products(token):
    response = requests.get(
        f"{API_URL}/products",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    if not response.ok:
        raise Exception(
            f"Failed to fetch products ({response.status_code})"
        )

    return response.json()


def get_product_by_id(product_id, token):
    response = requests.get(
        f"{API_URL}/products/{product_id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    if not response.ok:
        raise Exception(
            f"Failed to fetch product ({response.status_code})"
        )

    return response.json()

def get_buy_advice(product_id):

    response = requests.get(
        f"{API_URL}/ai/buy-advice/{product_id}"
    )

    if not response.ok:
        raise Exception(
            f"Failed to get AI advice ({response.status_code})"
        )

    return response.json()

def get_review_summary(product_id):

    response = requests.get(
        f"{API_URL}/ai/review-summary/{product_id}"
    )

    if not response.ok:
        raise Exception(
            f"Failed to get review summary ({response.status_code})"
        )

    return response.json()

def get_price_prediction(product_id):

    response = requests.get(
        f"{API_URL}/ai/price-prediction/{product_id}"
    )

    if not response.ok:
        raise Exception(
            f"Failed to get price prediction ({response.status_code})"
        )

    return response.json()

def get_alternatives(product_id):

    response = requests.get(
        f"{API_URL}/ai/alternatives/{product_id}"
    )

    if not response.ok:
        raise Exception(
            f"Failed to get alternatives ({response.status_code})"
        )

    return response.json()
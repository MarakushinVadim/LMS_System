import stripe

from LMS_System.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """
    Create a new product in Stripe
    """

    product = stripe.Product.create(name=product)
    return product


def create_stripe_price(amount):
    """
    Create a new price in Stripe
    """

    price = stripe.Price.create(
        unit_amount=int(amount) * 100,
        currency="rub",
        product_data={"name": "subscriptions"},
    )
    return price


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

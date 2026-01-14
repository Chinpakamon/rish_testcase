import stripe
from django.conf import settings


def create_checkout_session(item):
    stripe.api_key = settings.STRIPE_KEYS[item.currency]["secret"]

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": item.currency,
                "product_data": {
                    "name": item.name,
                    "description": item.description,
                },
                "unit_amount": item.price,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )

    return session

def create_order_checkout_session(order):
    currency = order.currency
    stripe.api_key = settings.STRIPE_KEYS[currency]["secret"]

    line_items = []
    for order_item in order.items.all():
        item_data = {
            "price_data": {
                "currency": currency,
                "product_data": {
                    "name": order_item.item.name,
                    "description": order_item.item.description,
                },
                "unit_amount": order_item.price_at_purchase,
            },
            "quantity": order_item.quantity,
        }

        if order.tax and order.tax.stripe_tax_rate_id:
            item_data["tax_rates"] = [order.tax.stripe_tax_rate_id]

        line_items.append(item_data)

    session_data = {
        "payment_method_types": ["card"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": "http://localhost:8000/success",
        "cancel_url": "http://localhost:8000/cancel",
        "metadata": {"order_id": order.id},
    }

    if order.discount and order.discount.stripe_coupon_id:
        session_data["discounts"] = [{"coupon": order.discount.stripe_coupon_id}]

    session = stripe.checkout.Session.create(**session_data)

    return session

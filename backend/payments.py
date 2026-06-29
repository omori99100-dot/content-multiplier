import os
import stripe
from .database import update_subscription, update_stripe_customer

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_IDS = {
    "basic": os.getenv("STRIPE_BASIC_PRICE_ID", "price_basic"),
    "pro": os.getenv("STRIPE_PRO_PRICE_ID", "price_pro"),
}

def create_checkout_session(user_id: int, plan: str, success_url: str, cancel_url: str) -> str | None:
    price_id = PRICE_IDS.get(plan)
    if not price_id:
        return None
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            metadata={"user_id": str(user_id), "plan": plan},
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return session.url
    except Exception as e:
        return None

def handle_checkout_completed(session: dict):
    metadata = session.get("metadata", {})
    user_id = int(metadata.get("user_id", 0))
    plan = metadata.get("plan", "free")
    customer_id = session.get("customer")
    subscription_id = session.get("subscription")
    if user_id:
        update_stripe_customer(user_id, customer_id)
        update_subscription(user_id, plan, subscription_id)

def handle_subscription_deleted(subscription: dict):
    metadata = subscription.get("metadata", {})
    user_id = int(metadata.get("user_id", 0))
    if user_id:
        update_subscription(user_id, "free")

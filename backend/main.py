from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ContentMultiplier AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

class RegisterRequest(BaseModel):
    username: str
    email: str
    name: str
    password: str
    referral_code: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class GenerateRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    tone: str = "professional"
    platforms: list[str] = ["twitter", "linkedin", "facebook"]
    language: str = "en"
    send_email: bool = False
    user_id: Optional[int] = None

class GenerateResponse(BaseModel):
    success: bool
    posts: dict[str, dict] = {}
    source_title: str = ""
    message: str = ""

def run_generation(user_id: int, url: str, text: str, tone: str, platforms: list[str], language: str, send_email: bool):
    source_text = text or ""
    source_title = ""
    if url:
        from utils.article_fetcher import fetch_article
        article = fetch_article(url)
        if article:
            source_text = article["text"]
            source_title = article["title"]
    if not source_text:
        return
    from utils.generator import generate_platform_posts
    posts = generate_platform_posts(source_text, platforms, tone, language)
    from .database import increment_daily_usage, save_generation, get_user_by_id
    increment_daily_usage(user_id)
    for platform, data in posts.items():
        save_generation(user_id, url or "", source_text[:500], source_title, platform, data["text"], tone, data.get("image_url"))
    if send_email:
        user = get_user_by_id(user_id)
        if user and user.get("email"):
            from utils.email_sender import send_results_email
            send_results_email(user["email"], {p: d["text"] for p, d in posts.items()}, source_title, language)

@app.get("/")
def root():
    return {"message": "ContentMultiplier AI API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/auth/register")
def register(req: RegisterRequest):
    from .auth import register_user
    result = register_user(req.username, req.email, req.name, req.password, req.referral_code)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"success": True, "user_id": result["user_id"]}

@app.post("/auth/login")
def login(req: LoginRequest):
    from .auth import authenticate_user
    user = authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "name": user["name"],
            "subscription": user["subscription"],
            "referral_code": user["referral_code"],
        },
    }

@app.get("/ref/{referral_code}")
def referral_redirect(referral_code: str):
    from .database import get_user_by_referral_code
    user = get_user_by_referral_code(referral_code)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid referral code")
    return RedirectResponse(url=f"{FRONTEND_URL}/?ref={referral_code}")

@app.get("/user/{user_id}/usage")
def get_usage(user_id: int):
    from .database import get_daily_usage, get_usage_limit
    used = get_daily_usage(user_id)
    limit = get_usage_limit(user_id)
    return {"used": used, "limit": limit, "remaining": limit - used}

@app.get("/user/{user_id}/history")
def get_history(user_id: int, limit: int = 20):
    from .database import get_generation_history
    history = get_generation_history(user_id, limit)
    return {"history": history}

@app.get("/user/{user_id}/referral")
def get_referral(user_id: int):
    from .database import get_referral_stats
    return get_referral_stats(user_id)

@app.post("/generate", response_model=GenerateResponse)
def generate_posts(req: GenerateRequest):
    if not req.url and not req.text:
        raise HTTPException(status_code=400, detail="Provide either a URL or text")
    if req.user_id:
        from .database import get_daily_usage, get_usage_limit
        used = get_daily_usage(req.user_id)
        limit = get_usage_limit(req.user_id)
        if used >= limit:
            raise HTTPException(status_code=402, detail=f"Daily limit reached ({limit}). Upgrade your plan for more.")
    source_text = req.text or ""
    source_title = ""
    if req.url:
        from utils.article_fetcher import fetch_article
        article = fetch_article(req.url)
        if not article:
            raise HTTPException(status_code=400, detail="Could not fetch article content")
        source_text = article["text"]
        source_title = article["title"]
    from utils.generator import generate_platform_posts
    posts = generate_platform_posts(source_text, req.platforms, req.tone, req.language)
    if req.user_id:
        from .database import increment_daily_usage, save_generation
        increment_daily_usage(req.user_id)
        for platform, data in posts.items():
            save_generation(req.user_id, req.url or "", source_text[:500], source_title, platform, data["text"], req.tone, data.get("image_url"))
    return GenerateResponse(success=True, posts=posts, source_title=source_title)

@app.post("/generate-async")
def generate_async(req: GenerateRequest, background_tasks: BackgroundTasks):
    if not req.url and not req.text:
        raise HTTPException(status_code=400, detail="Provide either a URL or text")
    if not req.user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    from .database import get_daily_usage, get_usage_limit
    used = get_daily_usage(req.user_id)
    limit = get_usage_limit(req.user_id)
    if used >= limit:
        raise HTTPException(status_code=402, detail=f"Daily limit reached ({limit}). Upgrade your plan for more.")
    background_tasks.add_task(run_generation, req.user_id, req.url or "", req.text or "", req.tone, req.platforms, req.language, req.send_email)
    msg = "جاري معالجة المحتوى. ستصل النتائج إلى بريدك الإلكتروني قريباً." if req.language == "ar" else "Processing your content. Results will be sent to your email shortly."
    return GenerateResponse(success=True, message=msg, source_title="")

@app.post("/create-checkout-session")
def create_checkout(data: dict):
    user_id = data.get("user_id")
    plan = data.get("plan", "basic")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id required")
    from .payments import create_checkout_session
    url = create_checkout_session(
        user_id, plan,
        success_url=data.get("success_url", f"{FRONTEND_URL}?checkout=success"),
        cancel_url=data.get("cancel_url", f"{FRONTEND_URL}?checkout=cancel"),
    )
    if not url:
        raise HTTPException(status_code=500, detail="Failed to create checkout session")
    return {"url": url}

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    import stripe
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if webhook_secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        import json
        event = json.loads(payload)

    from .payments import handle_checkout_completed, handle_subscription_deleted

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_completed(session)
        metadata = session.get("metadata", {})
        user_id = int(metadata.get("user_id", 0))
        plan = metadata.get("plan", "basic")
        if user_id:
            from .database import get_user_by_id, extend_subscription
            user = get_user_by_id(user_id)
            if user:
                from utils.email_sender import send_subscription_activated_email
                send_subscription_activated_email(user["email"], user["name"], plan, user.get("referral_code"), "ar")
                if user.get("referred_by"):
                    extend_subscription(user["referred_by"], 30)
    elif event["type"] == "customer.subscription.deleted":
        handle_subscription_deleted(event["data"]["object"])

    return {"received": True}

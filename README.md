
<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="License">
  <img src="https://img.shields.io/badge/status-MVP--ready-brightgreen" alt="Status">
</p>

<h1 align="center">🚀 ContentMultiplier AI</h1>
<p align="center"><strong>ضاعف محتواك لمنصات التواصل في دقائق بالذكاء الاصطناعي</strong></p>
<p align="center">Convert one article into platform-optimized social media posts — automatically.</p>

---

## 📋 Table of Contents | المحتويات

- [Features | الميزات](#features--الميزات)
- [Screenshots | لقطات شاشة](#screenshots--لقطات-شاشة)
- [Tech Stack | التقنيات](#tech-stack--التقنيات)
- [Quick Start | بداية سريعة](#quick-start--بداية-سريعة)
- [Project Structure | هيكل المشروع](#project-structure--هيكل-المشروع)
- [API Endpoints | نقاط النهاية](#api-endpoints--نقاط-النهاية)
- [Deployment | النشر](#deployment--النشر)
- [Contributing | المساهمة](#contributing--المساهمة)
- [License | الرخصة](#license--الرخصة)

---

## Features | الميزات

### 🌐 Bilingual | ثنائي اللغة
Full Arabic and English UI with RTL support and dialect options (Saudi, Egyptian).
واجهة عربية كاملة مع دعم RTL ولهجات سعودية ومصرية.

### 🤖 AI-Powered Generation | توليد بالذكاء الاصطناعي
Generate posts for Twitter/X, LinkedIn, Facebook, Instagram, and TikTok from a single article.
يولّد منشورات لجميع المنصات من مقال واحد.

### 📧 Email Delivery | توصيل بالإيميل
Results sent automatically to your inbox with a beautiful HTML template.
النتائج تصلك تلقائياً على بريدك الإلكتروني.

### 🖼️ Suggested Images | صور مقترحة
Automatic image suggestions from Unsplash for each post.
صور مقترحة تلقائياً لكل منشور.

### 🔗 Referral System | نظام إحالات
Refer friends and earn free months of subscription.
ادعُ أصدقاءك واربح أشهراً مجانية.

### 💳 Subscription Plans | خطط اشتراك
Free (5/day), Basic ($9/mo, 30/day), Pro ($29/mo, 100/day).
خطط: مجاني، أساسي $9، احترافي $29.

---

## Screenshots | لقطات شاشة

| Page | Screenshot |
|------|------------|
| 🏠 Landing Page | ![Landing](docs/screenshots/landing.png) |
| 🔐 Login | ![Login](docs/screenshots/login.png) |
| 🚀 Generate | ![Generate](docs/screenshots/generate.png) |
| 📊 Dashboard | ![Dashboard](docs/screenshots/dashboard.png) |
| 💎 Pricing | ![Pricing](docs/screenshots/pricing.png) |
| 🔗 Referrals | ![Referrals](docs/screenshots/referrals.png) |
| 📧 Email Template | ![Email](docs/screenshots/email.png) |

---

## Tech Stack | التقنيات

| Layer | Technology |
|-------|-----------|
| **Backend** | Python + FastAPI |
| **Frontend** | Streamlit |
| **AI** | OpenAI GPT-3.5-turbo |
| **Database** | SQLite |
| **Payments** | Stripe |
| **Email** | SendGrid |
| **Images** | Unsplash API |
| **Auth** | bcrypt + JWT |

---

## Quick Start | بداية سريعة

### Prerequisites | المتطلبات

- Python 3.11+
- OpenAI API key
- Stripe account (for subscriptions)
- SendGrid API key (for emails)
- Unsplash access key (for images)

### Installation | التنصيب

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/content-multiplier.git
cd content-multiplier

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start the backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# 5. Start the frontend (Terminal 2)
streamlit run frontend/app.py --server.port 8501

# 6. Open your browser
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Docker (Coming Soon)

```bash
docker-compose up
```

---

## Project Structure | هيكل المشروع

```
content-multiplier/
├── backend/
│   ├── main.py          ← FastAPI server (16 endpoints)
│   ├── auth.py          ← Registration & authentication
│   ├── database.py      ← SQLite ORM (4 tables)
│   └── payments.py      ← Stripe integration
├── frontend/
│   ├── app.py           ← User application (auth, generate, dashboard)
│   ├── landing.py       ← Marketing landing page
│   └── translations.py  ← Arabic/English dictionary (50+ keys)
├── utils/
│   ├── generator.py     ← AI post generation (6 tones, 5 platforms)
│   ├── article_fetcher.py ← URL article extraction
│   ├── email_sender.py  ← SendGrid HTML email templates
│   └── image_fetcher.py ← Unsplash image search
├── docs/
│   └── screenshots/     ← App screenshots
├── .env.example         ← Environment config template
├── requirements.txt     ← Python dependencies
└── run.py               ← Local dev runner
```

---

## API Endpoints | نقاط النهاية

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/auth/register` | User registration |
| POST | `/auth/login` | User login |
| GET | `/ref/{code}` | Referral redirect |
| GET | `/user/{id}/usage` | Daily usage stats |
| GET | `/user/{id}/history` | Generation history |
| GET | `/user/{id}/referral` | Referral stats |
| POST | `/generate` | Generate social posts |
| POST | `/generate-async` | Async generation |
| POST | `/create-checkout-session` | Stripe checkout |
| POST | `/stripe-webhook` | Stripe webhook |

---

## Deployment | النشر

### Option 1: Railway (Recommended)

```bash
# 1. Push to GitHub
git push origin main

# 2. Create Railway project
# - Connect GitHub repo
# - Add start command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# - Add environment variables from .env.example
```

### Option 2: Streamlit Cloud + Render

- Frontend: Streamlit Cloud (free)
- Backend: Render or Railway (free tier)

---

## Contributing | المساهمة

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

نرحب بمساهماتكم! راجع دليل المساهمة للمزيد.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License | الرخصة

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<p align="center">
  Made with ❤️ for content creators everywhere
  <br>
  <a href="mailto:hello@contentmultiplier.app">Contact</a> ·
  <a href="https://github.com/yourusername/content-multiplier/issues">Report Bug</a> ·
  <a href="https://github.com/yourusername/content-multiplier/issues">Request Feature</a>
</p>

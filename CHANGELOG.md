# Changelog

All notable changes to ContentMultiplier AI will be documented in this file.

## [1.0.0] - 2026-06-29

### Added
- FastAPI backend with 16 REST API endpoints
- AI-powered social media post generation (Twitter, LinkedIn, Facebook, Instagram, TikTok)
- Article fetching from URLs (newspaper3k + BeautifulSoup)
- 6 tone options: Professional, Casual, Marketing, Humorous, Saudi dialect, Egyptian dialect
- Bilingual UI: Full Arabic and English with RTL support
- User authentication system (bcrypt, registration, login)
- SQLite database with 4 tables (users, generations, daily_usage, referrals)
- Daily usage tracking with tiered limits (Free: 5, Basic: 30, Pro: 100)
- Stripe subscription integration (Basic $9/mo, Pro $29/mo)
- SendGrid email delivery for generated posts
- Unsplash image suggestions for each post
- Async background generation with FastAPI BackgroundTasks
- PDF export of generated posts
- Generation history dashboard
- Referral system with unique codes and free month rewards
- Professional landing page with hero, features, pricing, testimonials
- Privacy policy page (bilingual)
- Dockerfile for cloud deployment
- railway.json for Railway deployment
- Comprehensive README with bilingual documentation
- MIT License and contributing guidelines

### Technical
- Python 3.11 + FastAPI + Streamlit
- OpenAI GPT-3.5-turbo for content generation
- Stripe for payment processing
- SendGrid for transactional emails
- bcrypt for password hashing
- SQLite for data persistence
- 15 Python modules across 3 packages

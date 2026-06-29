# Contributing to ContentMultiplier AI | المساهمة

We love your input! We want to make contributing as easy and transparent as possible.

نرحب بمساهماتكم! نريد أن نجعل المساهمة سهلة وشفافة قدر الإمكان.

## How to Contribute | كيف تساهم

### 🐛 Report Bugs | أبلغ عن أخطاء

Open an issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

### 💡 Suggest Features | اقترح ميزات

Open an issue with:
- A clear title and description
- Why this would be useful
- How it might work

### 🔧 Submit Code Changes | أرسل تغييرات برمجية

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests: `python -m pytest` (if available)
5. Commit with clear messages
6. Push and open a Pull Request

## Code Style | أسلوب البرمجة

- Python: Follow PEP 8
- Use type hints where possible
- Add docstrings for functions
- Keep functions small and focused
- Test your changes locally

## Development Setup | إعداد بيئة التطوير

```bash
git clone https://github.com/yourusername/content-multiplier.git
cd content-multiplier
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn backend.main:app --reload --port 8000  # Terminal 1
streamlit run frontend/app.py --server.port 8501  # Terminal 2
```

## License | الرخصة

By contributing, you agree that your contributions will be licensed under the MIT License.

import os

client = None

def get_client():
    global client
    if client is None:
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
    return client

PLATFORM_PROMPTS = {
    "twitter": {
        "en": "Write a Twitter/X post (max 280 characters). Include 3-5 relevant hashtags. Make it engaging and concise.",
        "ar": "اكتب تغريدة تويتر (حد أقصى 280 حرفاً). أضف 3-5 هاشتاغات مناسبة. اجعلها جذابة وموجزة.",
    },
    "linkedin": {
        "en": "Write a LinkedIn post. Use a professional yet approachable tone. Include a hook, insights, and 3-5 hashtags. Aim for 150-300 words.",
        "ar": "اكتب منشور لينكدإن. استخدم نبرة مهنية لكن ودودة. ابدأ بمقدمة مشوقة، أضف تحليلات، و3-5 هاشتاغات. 150-300 كلمة.",
    },
    "facebook": {
        "en": "Write a Facebook post. Make it conversational and engaging. Include a question to drive comments. Add 3-5 hashtags. Aim for 100-200 words.",
        "ar": "اكتب منشور فيسبوك. اجعله حوارياً وجذاباً. أضف سؤالاً لتحفيز التعليقات. أرفق 3-5 هاشتاغات. 100-200 كلمة.",
    },
    "instagram": {
        "en": "Write an Instagram caption. Make it inspiring and visually descriptive. Include emojis and 5-10 hashtags. Keep it under 2200 characters.",
        "ar": "اكتب تعليق إنستغرام. اجعله ملهمًا ووصفيًا. أضف رموز تعبيرية و5-10 هاشتاغات. أقل من 2200 حرف.",
    },
    "tiktok": {
        "en": "Write a TikTok video script. Make it short, punchy, and trend-aware. Include hook, body, and CTA. Aim for 30-60 seconds.",
        "ar": "اكتب سيناريو فيديو تيك توك. اجعله قصيراً وقوياً. تضمن افتتاحية مشوقة، وجهاً، ودعوة للتفاعل. 30-60 ثانية.",
    },
}

TONE_INSTRUCTIONS = {
    "professional": {
        "en": "Use a professional, authoritative tone. Be confident and data-driven.",
        "ar": "استخدم نبرة مهنية موثوقة. كن واثقاً ومبيناً بالبيانات.",
    },
    "casual": {
        "en": "Use a friendly, casual tone as if talking to a friend. Be warm and approachable.",
        "ar": "استخدم نبرة ودية غير رسمية وكأنك تتحدث مع صديق. كن دافئاً وقريباً.",
    },
    "marketing": {
        "en": "Use a persuasive marketing tone. Create urgency and highlight benefits.",
        "ar": "استخدم نبرة تسويقية مقنعة. اخلق شعوراً بالإلحاح وأبرز الفوائد.",
    },
    "humorous": {
        "en": "Use a witty, humorous tone with light jokes and wordplay.",
        "ar": "استخدم نبرة فكاهية ذكية مع نكات خفيفة وجناس لفظي.",
    },
    "saudi": {
        "ar": "اكتب باللهجة السعودية المفهومة. استخدم تعابير سعودية أصيلة مثل 'والله'، 'بس'، 'اللي'. حافظ على الاحترافية.",
        "en": "Write in Saudi dialect. Use authentic Saudi expressions. Maintain professionalism.",
    },
    "egyptian": {
        "ar": "اكتب باللهجة المصرية العامية. استخدم تعابير مصرية مثل 'يعني'، 'بقى'، 'أهو'. حافظ على الاحترافية.",
        "en": "Write in Egyptian dialect. Use authentic Egyptian expressions. Maintain professionalism.",
    },
}

SYSTEM_PROMPTS = {
    "en": "You are a social media content strategist. Generate platform-optimized posts that drive engagement.",
    "ar": "أنت خبير تسويق محتوى عربي. تولد منشورات مخصصة لكل منصة بالعربية الفصحى أو العامية حسب الطلب. تجنب الترجمة الحرفية والركاكة. استخدم تعابير عربية أصيلة وجذابة.",
}

def generate_platform_posts(text: str, platforms: list[str], tone: str = "professional", language: str = "en") -> dict[str, dict]:
    if not text or len(text.strip()) < 20:
        return {p: {"text": "Error: Input text is too short.", "image_url": None} for p in platforms}

    ai_client = get_client()
    if ai_client is None:
        return {p: {"text": "OPENAI_API_KEY not set.", "image_url": None} for p in platforms}

    tone_instr = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["professional"])
    tone_text = tone_instr.get(language, tone_instr.get("en", ""))

    from utils.image_fetcher import fetch_image_for_post

    results = {}
    for platform in platforms:
        prompt_template = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["twitter"])
        platform_instruction = prompt_template.get(language, prompt_template.get("en", ""))

        system = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["ar"])

        full_prompt = f"{platform_instruction}\n\n{tone_text}\n\nContent:\n{text[:4000]}"

        try:
            response = ai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": full_prompt},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            post_text = response.choices[0].message.content.strip()
            image_url = fetch_image_for_post(post_text)
            results[platform] = {"text": post_text, "image_url": image_url}
        except Exception as e:
            results[platform] = {"text": f"Error: {str(e)}", "image_url": None}

    return results

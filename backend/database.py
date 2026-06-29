import sqlite3
import os
from datetime import datetime, date, timedelta
import secrets

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            subscription TEXT DEFAULT 'free',
            stripe_customer_id TEXT,
            stripe_subscription_id TEXT,
            referral_code TEXT UNIQUE,
            referred_by INTEGER,
            referral_count INTEGER DEFAULT 0,
            subscription_end DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referred_by) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source_url TEXT,
            source_text TEXT,
            source_title TEXT,
            platform TEXT NOT NULL,
            generated_content TEXT NOT NULL,
            image_url TEXT,
            tone TEXT DEFAULT 'professional',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS daily_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, date)
        );
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_id INTEGER NOT NULL,
            bonus_given INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users(id),
            FOREIGN KEY (referred_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

init_db()

def generate_referral_code() -> str:
    return secrets.token_hex(4).upper()

def create_user(username: str, email: str, name: str, hashed_password: str, referred_by: int | None = None) -> int | None:
    conn = get_connection()
    try:
        code = generate_referral_code()
        cur = conn.execute(
            "INSERT INTO users (username, email, name, hashed_password, referral_code, referred_by) VALUES (?, ?, ?, ?, ?, ?)",
            (username, email, name, hashed_password, code, referred_by),
        )
        user_id = cur.lastrowid
        if referred_by:
            conn.execute("UPDATE users SET referral_count = referral_count + 1 WHERE id = ?", (referred_by,))
            conn.execute(
                "INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)",
                (referred_by, user_id),
            )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_username(username: str) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_email(email: str) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_referral_code(code: str) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE referral_code = ?", (code,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_daily_usage(user_id: int) -> int:
    conn = get_connection()
    today = date.today().isoformat()
    row = conn.execute(
        "SELECT count FROM daily_usage WHERE user_id = ? AND date = ?",
        (user_id, today),
    ).fetchone()
    conn.close()
    return row["count"] if row else 0

def increment_daily_usage(user_id: int) -> int:
    conn = get_connection()
    today = date.today().isoformat()
    conn.execute(
        "INSERT INTO daily_usage (user_id, date, count) VALUES (?, ?, 1) "
        "ON CONFLICT(user_id, date) DO UPDATE SET count = count + 1",
        (user_id, today),
    )
    conn.commit()
    row = conn.execute(
        "SELECT count FROM daily_usage WHERE user_id = ? AND date = ?",
        (user_id, today),
    ).fetchone()
    conn.close()
    return row["count"] if row else 1

def get_usage_limit(user_id: int) -> int:
    conn = get_connection()
    user = conn.execute("SELECT subscription, subscription_end FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        return 0
    sub = user["subscription"]
    end = user["subscription_end"]
    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d").date() if isinstance(end, str) else end
        if end_date < date.today():
            return 5
    if sub == "pro":
        return 100
    if sub == "basic":
        return 30
    return 5

def save_generation(user_id: int, source_url: str, source_text: str, source_title: str, platform: str, content: str, tone: str, image_url: str | None = None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO generations (user_id, source_url, source_text, source_title, platform, generated_content, image_url, tone) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, source_url, source_text, source_title, platform, content, image_url, tone),
    )
    conn.commit()
    conn.close()

def get_generation_history(user_id: int, limit: int = 20) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM generations WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_subscription(user_id: int, plan: str, stripe_sub_id: str | None = None):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET subscription = ?, stripe_subscription_id = ? WHERE id = ?",
        (plan, stripe_sub_id, user_id),
    )
    conn.commit()
    conn.close()

def extend_subscription(user_id: int, days: int = 30):
    conn = get_connection()
    user = conn.execute("SELECT subscription_end FROM users WHERE id = ?", (user_id,)).fetchone()
    old_end = user["subscription_end"] if user and user["subscription_end"] else date.today().isoformat()
    if isinstance(old_end, str):
        old_end = datetime.strptime(old_end, "%Y-%m-%d").date()
    new_end = (old_end + timedelta(days=days)).isoformat()
    conn.execute("UPDATE users SET subscription_end = ? WHERE id = ?", (new_end, user_id))
    conn.commit()
    conn.close()

def update_stripe_customer(user_id: int, stripe_customer_id: str):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET stripe_customer_id = ? WHERE id = ?",
        (stripe_customer_id, user_id),
    )
    conn.commit()
    conn.close()

def get_referral_stats(user_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT referral_code, referral_count FROM users WHERE id = ?", (user_id,)).fetchone()
    bonuses = conn.execute(
        "SELECT COUNT(*) as cnt FROM referrals WHERE referrer_id = ? AND bonus_given = 1",
        (user_id,),
    ).fetchone()
    conn.close()
    return {
        "code": row["referral_code"] if row else "",
        "count": row["referral_count"] if row else 0,
        "bonuses": bonuses["cnt"] if bonuses else 0,
    }

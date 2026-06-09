import os

# SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./terranova.db")

# JWT
SECRET_KEY = os.getenv("SECRET_KEY", "terranova-dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Gamification
EXP_PER_KNOWLEDGE_POINT = 100
EXP_PER_STAR = 50
EXP_DAILY_QUEST_BONUS = 50
EXP_CHALLENGE_QUEST_BONUS = 200

LEVEL_THRESHOLDS = {
    "学徒": 0,
    "入门": 500,
    "进阶": 2000,
    "精通": 5000,
    "大师": 10000,
}

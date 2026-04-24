from datetime import datetime, timezone
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_DB_URL: str
    SUPABASE_PASSWORD: str

    UPSTASH_REDIS_URL: str
    UPSTASH_REDIS_TOKEN: str

    CLOUDFLARE_R2_ACCESS_KEY: str
    CLOUDFLARE_R2_SECRET_KEY: str
    CLOUDFLARE_R2_BUCKET: str = "mindtrack-notes"
    CLOUDFLARE_R2_ENDPOINT: str

    GOOGLE_VISION_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_SECRET: str = ""

    FCM_SERVER_KEY: str = ""

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()


def is_trial_active(trial_ends_at: datetime) -> bool:
    if trial_ends_at is None:
        return False
    now = datetime.now(timezone.utc)
    if trial_ends_at.tzinfo is None:
        trial_ends_at = trial_ends_at.replace(tzinfo=timezone.utc)
    return now < trial_ends_at

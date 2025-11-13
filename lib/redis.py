from upstash_redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()


def get_redis_client() -> Redis:
    redis = Redis.from_env()
    return redis

def get_memory_key(user_email: str) -> str:
    return f"memory:{user_email}"

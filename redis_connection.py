import os

import redis
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host=os.environ.get("REDIS_HOST"),
                port=os.environ.get("REDIS_PORT"),
                username=os.environ.get("REDIS_USERNAME"),
                password=os.environ.get("REDIS_PASSWORD"))

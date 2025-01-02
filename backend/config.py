# config.py
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class LocalDevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECURITY_JOIN_USER_ROLES = 'roles_users'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    JWT_SECRET_KEY = '5#y2LF4Q8z\n\xec]/'
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CELERY_BROKER_URL = "redis://localhost:6379/8"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/9"
    CELERY_TIMEZONE = "Asia/Kolkata"
    REDIS_URL = "redis://localhost"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 6
    CACHE_DEFAULT_TIMEOUT = 300

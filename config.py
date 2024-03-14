import os
from dataclasses import dataclass, asdict

from dotenv import load_dotenv

load_dotenv('../.env/.env.local')


@dataclass
class BaseConfig:
    def asdict(self):
        return asdict(self)


@dataclass
class DatabaseConfig(BaseConfig):
    """Database connection variables"""
    NAME: str = os.getenv('DB_NAME')
    USER: str = os.getenv('DB_USER')
    PASSWD: str = os.getenv('DB_PASSWORD')
    HOST: str = os.getenv('DB_HOST')
    PORT: str = os.getenv('DB_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWD}@{self.HOST}:{self.PORT}/{self.NAME}"


@dataclass
class BotConfig(BaseConfig):
    """Bot configuration"""
    BASE_URL: str = os.getenv('BASE_URL')
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    PAYMENT_CLICK_TOKEN: str = os.getenv('PAYMENT_CLICK_TOKEN')

    WEB_SERVER_HOST: str = "127.0.0.1"
    WEB_SERVER_PORT: int = 8080
    MAIN_BOT_PATH: str = "/webhook/main"
    OTHER_BOTS_PATH: str = "/webhook/bot/{bot_token}"

    OTHER_BOTS_URL: str = f"{BASE_URL}{OTHER_BOTS_PATH}"


@dataclass
class RedisConfig(BaseConfig):
    """Redis configuration"""
    URL: str = os.getenv('REDIS_URL')
    DB: str = os.getenv('REDIS_DB')
    HOST: str = os.getenv('REDIS_HOST')
    PORT: str = os.getenv('REDIS_PORT')


@dataclass
class WebConfig(BaseConfig):
    """Web configuration"""
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    USERNAME: str = os.getenv('ADMIN_USERNAME')
    PASSWD: str = os.getenv('ADMIN_PASSWORD')


@dataclass
class Configuration:
    """All in one configuration's class"""
    rd = RedisConfig()
    db = DatabaseConfig()
    bot = BotConfig()
    web = WebConfig()


conf = Configuration()

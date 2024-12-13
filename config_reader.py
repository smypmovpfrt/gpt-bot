from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

user_contexts = {}
user_settings = {}


class Settings(BaseSettings):
    bot_token: SecretStr
    base_url: str
    api_key: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
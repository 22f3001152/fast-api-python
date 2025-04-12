import os

from pydantic_settings import BaseSettings

env = os.environ.get("ENVIRONMENT", "development").lower()


class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = True
    db_uri: str

    class Config:
        env_file = ".env"


class DevelopmentSettings(Settings):
    debug: bool = True

    class Config:
        env_file = ".env.dev"


class TestingSettings(Settings):
    debug: bool = True

    class Config:
        env_file = ".env.test"


class ProductionSettings(Settings):
    debug: bool = False

    class Config:
        env_file = ".env.prod"


def get_settings() -> Settings:
    """
    Get the settings based on the current environment.
    """
    settings = {
        "development": DevelopmentSettings,
        "testing": TestingSettings,
        "production": ProductionSettings,
    }

    if env not in settings:
        raise ValueError(
            f"Invalid environment: {env}. Expected one of {list(settings.keys())}."
        )

    return settings[env]()

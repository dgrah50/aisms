import os

ENV = os.getenv("ENVIRONMENT", "production")


def get_database_url():
    if ENV == "development":
        return "sqlite://:memory:"  # Using in-memory database for tests
    else:
        return "sqlite://sms_chatbot.db"  # Default path for non-test environments


class ConfigurationError(Exception):
    pass

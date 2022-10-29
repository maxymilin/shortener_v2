from os import getenv

from dotenv import load_dotenv

from app.core.config import Settings

# Python-dotenv package to load the .env file and
# be able to set different env files in Dockerfile instructions in future.
load_dotenv(getenv("ENV_FILE"))

settings = Settings()

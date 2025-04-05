import os

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{DB_PATH}"},
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
        },
    },
}
API_PORT = int(os.getenv("API_PORT"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")  # TODO: remove

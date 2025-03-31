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
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

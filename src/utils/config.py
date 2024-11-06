import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

BOT_TOKEN = os.getenv("TOKEN")
OWNER_IDS = []


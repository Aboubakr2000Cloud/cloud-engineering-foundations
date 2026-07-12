# config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # loads the .env file

# API key from .env
API_KEY = os.getenv("API_KEY")

# Default settings
DEFAULT_CITIES = ["London", "Paris", "Tokyo"]
LOG_FILE = "logs/app.log"
DATA_DIR = Path("data")

#Constants
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_UNITS = "metric"
REQUEST_TIMEOUT = 10

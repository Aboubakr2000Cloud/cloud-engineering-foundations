#!/usr/bin/env python3
import requests
import logging
import datetime
import json
import time
import argparse
from config import API_KEY, DEFAULT_CITIES, LOG_FILE, DATA_DIR, BASE_URL, DEFAULT_UNITS, REQUEST_TIMEOUT
from pathlib import Path
from enum import Enum

class FetchResult(Enum):
    SUCCESS = "success"
    NETWORK_ERROR = "network_error"
    NOT_FOUND = "not_found"
    INVALID_CONFIG = "invalid_config"
    GLOBAL_NETWORK_FAILURE = "global_network_failure"

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

PARAMETER_MAP = {
       "temperature": lambda d: d["main"]["temp"],
       "humidity": lambda d: d["main"]["humidity"],
       "pressure": lambda d: d["main"]["pressure"],
       "description": lambda d: d["weather"][0]["description"],
       "wind_speed": lambda d: d["wind"]["speed"],
     }

PARAMETER_CHOICES = list(PARAMETER_MAP.keys())

def fetch_weather(city):
   logger.info("Starting data fetch...")
   params = {
       "q": city,
       "appid": API_KEY,
       "units": DEFAULT_UNITS,
   }

   try:
       response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
       response.raise_for_status()
       logger.info("API call successful!")
       data = response.json()
       logger.info(f"Fetched weather data for {data['name']}")
       return FetchResult.SUCCESS, data

   except requests.exceptions.HTTPError as e:
       if response.status_code == 404:
          logger.error(f"City not found (404): {e}")
          return FetchResult.NOT_FOUND, None
       else:
           logger.error(f"HTTP Error: {e}")
           return FetchResult.NETWORK_ERROR, None
   except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
          logger.warning(f"Network error occurred: {e}")
          return FetchResult.NETWORK_ERROR, None
   except requests.exceptions.RequestException as e:
          logger.error(f"Unexpected error occurred: {e}")
          return FetchResult.NETWORK_ERROR, None

def retry_fetch(city, max_retries=3):
    for attempt in range(1, max_retries + 1):

        logger.info(f"Attempt {attempt} to fetch weather for {city}!")
        status, data = fetch_weather(city)

        if status == FetchResult.NOT_FOUND:
           logger.critical(f"Retry aborted for {city}: {status.name}")
           return status, None

        if status == FetchResult.SUCCESS:
           return FetchResult.SUCCESS, data

        if attempt < max_retries:
           wait_time = 2 ** attempt
           logger.warning(f"Attempt {attempt} failed. Retrying in {wait_time} seconds...")
           time.sleep(wait_time)
        else:
            logger.error("All retries failed due to network error! Treating as global failure.")

    return FetchResult.GLOBAL_NETWORK_FAILURE, None

def process_data(data, params):
    processed_data = []

    if not data:
        return []

    weather_entry = {
            "city": data['name'],
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    for p in params:
        weather_entry[p] = PARAMETER_MAP[p](data)

    processed_data.append(weather_entry)

    return processed_data

def save_to_file(processed_data):
   try:
       DATA_DIR.mkdir(parents=True, exist_ok=True)

       timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
       filename = DATA_DIR / f"weather_{timestamp}.json"

       with open(filename, 'w') as f:
            json.dump(processed_data, f, indent=4)

       logger.info(f"Saved data to {filename}")

   except (IOError, OSError) as e:
       logger.error(f"File write error: {e}")

   return filename

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="🌤️ Weather Fetcher CLI\nFetch weather data for one or more cities with selected parameters.",
        epilog=(
            "💡 Examples:\n"
            "  python weather.py London Paris --parameters temperature humidity\n"
            "  python weather.py Tokyo --dry-run\n"
            "  python weather.py New_York --parameters description wind_speed\n\n"
            "Choose parameters from: temperature, humidity, pressure, description, wind_speed"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "cities",
        nargs="+",
        help="Provide one or more cities (e.g., London Paris New_York)"
    )

    parser.add_argument(
        "--parameters",
        choices=PARAMETER_CHOICES,
        nargs="+",
        default=["temperature", "description", "wind_speed"],
        help="Select which weather parameters to fetch (default: temperature, description, wind_speed)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate fetching data without saving to file"
    )

    return parser.parse_args()


def main():
   if not API_KEY:
       logger.critical(
           "Missing API key. Set OPENWEATHER_API_KEY in .env file."
       )
       return

   success_cities = []
   failed_cities = []
   all_processed_data = []

   arguments = parse_arguments()
   params = arguments.parameters
   cities = arguments.cities if arguments.cities else DEFAULT_CITIES
   dry_run = arguments.dry_run

   for city in cities:

       status, data = retry_fetch(city)

       if status == FetchResult.GLOBAL_NETWORK_FAILURE:
           logger.critical(
               "Cannot proceed with other cities due to global network failure"
           )
           failed_cities.append(city)
           break

       if status != FetchResult.SUCCESS:
           logger.critical(f"Skipping {city} due to fetch failure")
           failed_cities.append(city)
           continue

       processed = process_data(data, params)

       if dry_run:
          logger.info(f"[Dry-run] Would save data for {city}: {processed}")
       else:
          all_processed_data.extend(processed)
          success_cities.append(city)

   if not dry_run and all_processed_data:
       save_to_file(all_processed_data)
   else:
       logger.warning("No data to save!")
   
   logger.info("=== Fetch Summary ===")
   logger.info(f"Successful: {', '.join(success_cities) if success_cities else 'None'}")
   logger.info(f"Failed: {', '.join(failed_cities) if failed_cities else 'None'}")

if __name__ == "__main__":
    main()


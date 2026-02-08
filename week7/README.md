# Week 7 — Python for Automation & APIs

## Overview

This week focused on integrating Python with external APIs and implementing production-ready automation patterns. The project demonstrates real-world API consumption, intelligent error handling, retry logic with exponential backoff, and professional logging practices.

**Key Learning Areas:**
- HTTP requests with the `requests` library
- API authentication and parameter handling
- JSON parsing and data processing
- Professional logging (console + file)
- Retry logic with exponential backoff
- Command-line argument parsing
- Environment variable management
- Error classification and handling strategies

---

## Project: Weather Data Fetcher CLI

A professional command-line tool that fetches current weather data from OpenWeatherMap API for multiple cities, processes the data based on user-selected parameters, implements intelligent retry logic, and saves results to timestamped JSON files.

### Project Structure

```
Cloud-learning-project/
│
├── weather.py              # Main application script
├── config.py               # Configuration and settings
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
│
├── logs/                   # Log files directory
│   └── app.log             # Application logs
│
└── data/                   # Output JSON files
    └── weather_YYYY-MM-DD_HHMMSS.json
```

---

## Features

✅ **Multi-City Support** - Fetch weather data for multiple cities in a single run  
✅ **Flexible Parameters** - Choose which weather metrics to retrieve (temperature, humidity, pressure, wind speed, description)  
✅ **Intelligent Retry Logic** - Exponential backoff with configurable max retries  
✅ **Error Classification** - Distinguishes between retryable (network errors) and non-retryable errors (404, missing config)  
✅ **Global Failure Detection** - Stops execution early if network is globally unavailable  
✅ **Professional Logging** - Dual output to console and file with appropriate log levels  
✅ **Dry-Run Mode** - Test execution without saving data  
✅ **Timestamped Output** - JSON files with human-readable timestamps  
✅ **CLI Interface** - Full argparse implementation with help text and examples  
✅ **Secure Configuration** - API keys stored in `.env` file (never committed)

---

## Usage

### Basic Organization

Activate virtual environment and install dependencies:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "API_KEY=your_openweathermap_api_key" > .env
```

Get your free API key from: https://openweathermap.org/api

### Command-Line Arguments

**Fetch weather for specific cities:**
```bash
python weather.py London Paris Tokyo
```

**Select custom parameters:**
```bash
python weather.py Berlin --parameters temperature humidity wind_speed
```

**Available parameters:**
- `temperature` - Temperature in Celsius
- `humidity` - Humidity percentage
- `pressure` - Atmospheric pressure
- `description` - Weather description (e.g., "clear sky")
- `wind_speed` - Wind speed in m/s

**Dry-run mode (test without saving):**
```bash
python weather.py London --dry-run
```

**Cities with spaces:**
```bash
python weather.py "New York" "Los Angeles"
```

**Full help:**
```bash
python weather.py --help
```

### Example Session

```bash
$ python weather.py London Paris Tokyo --parameters temperature description

2025-02-08 14:23:15 - INFO - Attempt 1 to fetch weather for London!
2025-02-08 14:23:15 - INFO - Starting data fetch...
2025-02-08 14:23:16 - INFO - API call successful!
2025-02-08 14:23:16 - INFO - Fetched weather data for London
2025-02-08 14:23:16 - INFO - Attempt 1 to fetch weather for Paris!
2025-02-08 14:23:16 - INFO - Starting data fetch...
2025-02-08 14:23:17 - INFO - API call successful!
2025-02-08 14:23:17 - INFO - Fetched weather data for Paris
2025-02-08 14:23:17 - INFO - Attempt 1 to fetch weather for Tokyo!
2025-02-08 14:23:17 - INFO - Starting data fetch...
2025-02-08 14:23:18 - INFO - API call successful!
2025-02-08 14:23:18 - INFO - Fetched weather data for Tokyo
2025-02-08 14:23:18 - INFO - Saved data to data/weather_2025-02-08_142318.json
2025-02-08 14:23:18 - INFO - === Fetch Summary ===
2025-02-08 14:23:18 - INFO - Successful: London, Paris, Tokyo
2025-02-08 14:23:18 - INFO - Failed: None
```

**Output JSON:**
```json
[
    {
        "city": "London",
        "time": "2025-02-08 14:23:18",
        "temperature": 12.5,
        "description": "clear sky"
    },
    {
        "city": "Paris",
        "time": "2025-02-08 14:23:18",
        "temperature": 14.2,
        "description": "few clouds"
    },
    {
        "city": "Tokyo",
        "time": "2025-02-08 14:23:18",
        "temperature": 8.7,
        "description": "overcast clouds"
    }
]
```

---

## What It Does

1. **Validates Configuration** - Checks for API key in environment variables
2. **Processes Cities** - Iterates through provided city list
3. **Fetches Weather Data** - Makes authenticated API calls to OpenWeatherMap
4. **Implements Retry Logic** - Retries network failures with exponential backoff (2s, 4s, 8s)
5. **Classifies Errors** - Distinguishes between:
   - Retryable errors (network timeout, connection issues)
   - Non-retryable errors (404 city not found, missing API key)
   - Global failures (API endpoint unreachable)
6. **Processes Data** - Extracts user-selected parameters using lambda mapping
7. **Saves Results** - Writes to timestamped JSON file with proper formatting
8. **Logs Everything** - Comprehensive logging to both console and `logs/app.log`
9. **Generates Summary** - Reports successful and failed cities

---

## Skills Demonstrated

✅ **API Integration** - RESTful API consumption with authentication  
✅ **HTTP Methods** - GET requests with query parameters and headers  
✅ **JSON Handling** - Parsing and serializing JSON data  
✅ **Error Handling** - Multi-level exception handling with specific error types  
✅ **Retry Patterns** - Exponential backoff implementation  
✅ **Logging Best Practices** - Structured logging with appropriate levels (INFO, WARNING, ERROR, CRITICAL)  
✅ **CLI Development** - argparse with subcommands and help documentation  
✅ **Configuration Management** - Environment variables with python-dotenv  
✅ **File I/O** - Dynamic file creation with timestamps  
✅ **Code Organization** - Separation of concerns (config, logic, I/O)  
✅ **Security** - API key management without hardcoding  
✅ **Lambda Functions** - Functional programming for data extraction  

---

## Technical Highlights

### 1. Parameter Mapping Strategy
```python
PARAMETER_MAP = {
    "temperature": lambda d: d["main"]["temp"],
    "humidity": lambda d: d["main"]["humidity"],
    "pressure": lambda d: d["main"]["pressure"],
    "description": lambda d: d["weather"][0]["description"],
    "wind_speed": lambda d: d["wind"]["speed"],
}
```
Using lambda functions for dynamic parameter extraction provides flexibility and eliminates repetitive conditional logic.

### 2. Error Classification System
```python
class FetchResult(Enum):
    SUCCESS = "success"
    NETWORK_ERROR = "network_error"
    NOT_FOUND = "not_found"
    INVALID_CONFIG = "invalid_config"
    GLOBAL_NETWORK_FAILURE = "global_network_failure"
```
Intelligent error categorization prevents wasting retries on unrecoverable errors.

### 3. Global Failure Detection
```python
if data == "GLOBAL_NETWORK_FAILURE":
    logger.critical("Aborting execution: global network failure detected.")
    break
```
Stops processing remaining cities when API endpoint is unreachable, saving time and resources.

### 4. Exponential Backoff
```python
wait_time = 2 ** attempt  # 2, 4, 8 seconds
time.sleep(wait_time)
```
Standard retry pattern that reduces server load and increases success probability.

---

## Testing

The script handles various failure scenarios:

**✅ Invalid City (404 Error):**
```bash
python weather.py InvalidCity123
# Logs error, does not retry, continues to next city
```

**✅ Missing API Key:**
```bash
# Remove API_KEY from .env
python fetcher.py London
# Logs critical error, aborts immediately
```

**✅ Network Timeout:**
```bash
# Simulated by modifying URL endpoint
# Triggers retry logic with exponential backoff
```

**✅ Global Network Failure:**
```bash
# Complete API endpoint failure
# Aborts after first city to avoid wasting retries
```

**✅ Dry-Run Mode:**
```bash
python weather.py London --dry-run
# Fetches data but doesn't save to file
```

---

## Error Handling

### HTTP Errors
- **404 Not Found** → City doesn't exist, skip without retry
- **401 Unauthorized** → Invalid API key, abort execution
- **500 Server Error** → Retry with backoff

### Network Errors
- **Connection Error** → Retry with exponential backoff
- **Timeout** → Retry with exponential backoff
- **DNS Resolution Failure** → Treated as global failure

### File I/O Errors
- **Permission Denied** → Log error, continue execution
- **Disk Full** → Log critical error

### Configuration Errors
- **Missing API Key** → Abort immediately with clear message
- **Invalid .env Format** → Log warning, attempt to continue

---

## Project Files

**`weather.py`** - Main application logic with CLI interface  
**`config.py`** - Centralized configuration (API key, defaults, paths)  
**`.env`** - Environment variables (not committed to Git)  
**`requirements.txt`** - Python dependencies with version pinning  
**`.gitignore`** - Excludes sensitive files (.env, logs, data)  
**`logs/app.log`** - Application log file with timestamps  
**`data/weather_*.json`** - Output files with weather data  

---

**Week 7 Complete!** This project demonstrates professional API integration with production-ready error handling, retry logic, and logging practices. The code showcases intelligent failure mode analysis with global network detection, preventing wasted retry attempts. Skills acquired this week are fundamental to cloud automation, infrastructure monitoring, and DevOps workflows. 


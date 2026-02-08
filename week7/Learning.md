# Week 7 — Python for Automation & APIs key Learnings

A Python command-line tool that fetches weather data from an external API, processes it safely, and stores structured results in JSON format.

This project was built incrementally to practice:
- HTTP requests
- Error handling
- Retry logic
- Logging
- Configuration management
- CLI design (argparse)
- Clean project architecture

The goal is not just to fetch data, but to write robust, production-style code.


## Project Overview

This script allows users to:
- Fetch weather data for one or multiple cities
- Select specific weather parameters (temperature, humidity, etc.)
- Handle network failures and API errors correctly
- Retry only when appropriate
- Run in dry-run mode (no files written)
- Produce structured logs and summaries


## What I Learned


### 1. Making HTTP Requests with requests

Using the requests library to interact with REST APIs.

Common methods:
```python
    requests.get(url)
    requests.post(url, json=data)
```

Important response attributes:
```python
    response.status_code
    response.json()
    response.text
```

Key takeaway:
HTTP status codes indicate transport success/failure.
JSON content must still be validated separately.


### 2. JSON Structure Awareness

APIs do not always return the same structure.

Possible structures:
```python
    { "name": "London" }

    [
      {"id": 1},
      {"id": 2}
    ]
```

Learned to:
- Inspect API responses
- Slice lists:
```python
    posts[:3]
```
- Access nested data safely:
```pyhton
    data["weather"][0]["description"]
```

This was critical for extracting weather parameters correctly.


### 3. URL Parameters (params)

Instead of manually building URLs:
```python
   requests.get(url, params={"userId": 1})
```

Key lesson:
Not all APIs support all parameters.
Some APIs silently ignore unsupported parameters.


### 4. Error Handling (Professional Level)

Using:

    response.raise_for_status()

Handled cases:
- 404 Not Found
- Network errors
- Timeouts
- Generic request failures

Important realization:
HTTP status codes are not the same as a "status" key inside JSON.


### 5. Authentication Basics

APIs authenticate scripts, not humans.

Examples:
- API keys
- Bearer tokens in headers
```python
    headers = {
        "Authorization": "Bearer YOUR_TOKEN"
    }
```

Key understanding:
Scripts access APIs.
Browsers authenticate users.
These are different systems.


### 6. Logging

Implemented structured logging using the logging module.

Features:
- Console logging
- File logging
- Log levels:
  - INFO
  - WARNING
  - ERROR
  - CRITICAL

Example:
```python
    logger.info("Starting data fetch")
    logger.warning("Retrying after network failure")
    logger.critical("API key missing")
```

Logging greatly improved debugging and traceability.


### 7. Retry Logic

Retries are applied only when they make sense.

Retry policy:

- Network error      -> retry
- Timeout            -> retry
- 404 city not found -> do not retry
- Invalid API key    -> do not retry

Implemented exponential backoff:
```python
    wait_time = 2 ** attempt
    time.sleep(wait_time)
```

This avoids hammering the API.


### 8. Global Network Failure Detection

Problem:
If the network is down, retrying every city is pointless.

Solution:
- Detect global network failure
- Abort remaining cities
- Log a clear explanation

This improved efficiency and clarity.


### 9. Clean Architecture and Separation of Concerns

Project structure follows clear responsibilities:

- config.py       -> configuration and constants
- fetch_weather() -> API calls only
- retry_fetch()   -> retry policy
- process_data()  -> data transformation
- save_to_file()  -> persistence
- parse_arguments()  -> CLI interface
- main()          -> orchestration

This mirrors real production code.


### 10. Reusable API Client Pattern

Learned how to:
- Centralize base URLs
- Centralize headers
- Centralize authentication

This pattern scales well as projects grow.


### 11. Pagination Concept

Some APIs return data in pages.

Learned loop logic:
```python
    page = 1
    while True:
        data = fetch(page)
        if not data:
            break
        page += 1
```

## Command-Line Interface (CLI)

The script uses argparse for a clean CLI.

Examples:
```python
    python weather.py London Paris --parameters temperature humidity

    python weather.py Tokyo --dry-run
```

Features:
- Multiple cities
- Controlled parameter choices
- Helpful --help output
- Safe defaults


## Output

- Weather data saved as JSON
- Timestamped filenames
- Clean, structured format


## Challenges Faced and Solutions

Problem:
Retrying 404 errors.

Solution:
Explicit non-retry classification.

---

Problem:
Mixing network errors and configuration errors.

Solution:
Clear separation of failure reasons.

---

Problem:
Script stopped on first city failure.

Solution:
Use continue instead of return.

---

Problem:
Same network error repeated for all cities.

Solution:
Detect global network failure and abort early.


## Final Outcome

This project helped me:
- Think like a backend engineer
- Write resilient Python scripts
- Design clean APIs and CLIs
- Anticipate edge cases
- Build software that fails gracefully

Week 7 Complete! 



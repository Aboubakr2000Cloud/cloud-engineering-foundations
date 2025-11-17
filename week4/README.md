# Week 4 — Bash Scripting & Crontab

## Overview
Week 4 focuses on advanced bash scripting and automation through cron scheduling. The capstone project is a comprehensive website health monitoring system that automatically checks multiple websites, logs their status, detects issues, and generates daily summary reports—all running autonomously via cron jobs.

## Project: Website Health Monitor

A production-ready monitoring solution that tracks website availability, response times, and HTTP status codes across multiple endpoints. The system runs continuously via cron, maintaining historical logs and generating detailed daily reports.

### Project Structure
```
cloud-learning-project/
├── configs/
│   └── websites.conf           # Website configuration (URL, name, threshold)
├── logs/
│   ├── health.log              # All health check results
│   ├── errors.log              # Failed checks only
│   └── daily_reports/          # Daily summary reports
│       └── report_YYYY-MM-DD.txt
└── scripts/
    └── bash/
        └── health_monitor.sh   # Main monitoring script
```

## Features

### Core Monitoring
- **Multi-site checking**: Monitor unlimited websites from a simple config file
- **HTTP/HTTPS support**: Tests both protocols with configurable timeouts
- **Response time tracking**: Measures and logs response times in milliseconds
- **Threshold detection**: Identifies slow responses based on per-site thresholds
- **Status code validation**: Detects HTTP errors (4xx, 5xx) and connection failures

### Logging & Reporting
- **Timestamped logs**: Every check recorded with precise timestamps
- **Dual logging**: Separate logs for all checks and errors only
- **Daily reports**: Automated summary with statistics:
  - Total checks performed
  - Success rate percentage
  - Average response time
  - Sites with issues (unreachable, failed, slow)
  - Top 3 slowest sites

### Automation & Interface
- **Cron integration**: Fully automated execution (checks every 5 min, reports daily)
- **Command-line interface**: Professional CLI with multiple commands
- **User feedback**: Clear messages showing where results are saved

## Usage

### Commands
```bash
# Make script executable
chmod +x health_monitor.sh

# Run health checks manually
./health_monitor.sh check

# Generate daily report
./health_monitor.sh report

# Show current status of all sites
./health_monitor.sh status

# Display help
./health_monitor.sh help
```

### Configuration
Edit `configs/websites.conf` to add/remove sites:
```
# Format: URL,NAME,MAX_RESPONSE_TIME_MS
https://google.com,Google,2000
https://github.com,GitHub,3000
https://amazon.com,Amazon,2000
```

### Cron Schedule
Monitoring runs automatically via cron:
```bash
# Health checks every 5 minutes
*/5 * * * * /path/to/health_monitor.sh check

# Daily report at midnight
0 0 * * * /path/to/health_monitor.sh report
```

## What It Does

1. **Monitors Websites**: Every 5 minutes, checks all configured sites for:
   - Availability (can it be reached?)
   - HTTP status (200 OK, 404 Not Found, etc.)
   - Response speed (how fast did it respond?)

2. **Detects Issues**: Automatically identifies:
   - Unreachable sites (connection failures)
   - HTTP errors (4xx client errors, 5xx server errors)
   - Slow responses (exceeding configured thresholds)

3. **Logs Everything**: Maintains detailed records:
   - `health.log`: Complete history of all checks
   - `errors.log`: Failed checks for quick troubleshooting

4. **Reports Daily**: At midnight, generates comprehensive report:
   - How many checks ran today
   - What percentage succeeded
   - Average response time across all sites
   - Which sites had problems
   - Which sites were slowest

5. **Runs Autonomously**: Once configured, requires no manual intervention—cron handles everything automatically.

## Skills Demonstrated

### Bash Scripting
- ✅ Functions and modular code organization
- ✅ Variables and configuration management
- ✅ Control flow (if/else, case statements, loops)
- ✅ Exit codes and error handling
- ✅ Command-line argument parsing

### Text Processing
- ✅ grep: Pattern matching and filtering
- ✅ awk: Field extraction and calculations
- ✅ sed: Text substitution and cleaning
- ✅ cut: Column-based data extraction

### System Integration
- ✅ Cron job scheduling and automation
- ✅ File I/O operations (reading configs, writing logs)
- ✅ Timestamp handling with `date` command
- ✅ curl: HTTP requests with timing metrics

### Data Analysis
- ✅ Log parsing and aggregation
- ✅ Statistical calculations (averages, percentages)
- ✅ Sorting and ranking data
- ✅ Report generation from raw logs

## Project Files

### `health_monitor.sh`
Main script with four operational modes:
- `check`: Executes health checks on all configured sites
- `report`: Generates daily summary report from logs
- `status`: Shows current status of all monitored sites
- `help`: Displays usage instructions

### `configs/websites.conf`
CSV-format configuration file defining monitored sites:
- Column 1: Full URL (http:// or https://)
- Column 2: Display name
- Column 3: Maximum acceptable response time (milliseconds)

### `logs/health.log`
Continuous log of all health checks with format:
```
[YYYY-MM-DD HH:MM:SS] SiteName - SPEED (status: CODE (RESULT), TIME: XXms)
```

### `logs/errors.log`
Filtered log containing only failed checks (unreachable sites, HTTP errors, slow responses).

### `logs/daily_reports/report_YYYY-MM-DD.txt`
Daily summary report with statistics and analysis of the day's monitoring data.

---

**Week 4 Complete!**

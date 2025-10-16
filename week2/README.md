# Week 2: Log Analysis Project

## Overview
Automated log analysis tool that parses server logs and generates comprehensive reports identifying errors, security issues, and system health warnings.

## Project Structure
```
week2/
├── server.log              # Sample log file
├── analyze_log.sh          # Main analysis script
├── report.txt              # Generated report
├── commands.txt            # Command reference
└── README.md               # This file
```

## Features
- Error frequency analysis
- Failed login detection (security monitoring)
- Database connection monitoring
- System resource warnings (memory, disk, performance)
- Automated report generation

## Usage
```bash
cd scripts/bash
chmod +x analyze_log.sh
./analyze_log.sh logs/server.log
cat logs/report.txt
```
## Quick Start
From repository root:
```bash
./scripts/bash/analyze_log.sh logs/server.log
```

## Requirements
- Linux/Unix environment
- Standard tools: grep, awk, sort, uniq, wc

## Skills Demonstrated
- Log parsing and pattern matching
- Text processing with AWK
- Data aggregation and sorting
- Shell scripting
- Report generation

## Sample Output
```
LOG ANALYSIS REPORT
Date: Wed Oct 13 16:00:00 2025
=== SUMMARY: ===
- Total lines: 25
- ERROR count: 11
- WARNING count: 5
- INFO count: 9
...
``` 

## Challenges faced and solutions

### Challenge 1: Counting Most Common Errors
**Problem:** Initial `uniq -c` showed all errors with count "1" because timestamps made every line unique.

**Solution:** Used `awk` to extract only the error description columns (5, 6, 7), ignoring timestamps and IPs, then counted occurrences.

### Challenge 2: Detecting Memory Trends
**Problem:** Needed automated way to detect if memory usage was increasing (not just manually comparing percentages).

**Solution:** Created AWK script that compares each value to previous value, tracks increases/decreases, and outputs trend analysis.

### Challenge 3: Finding Root Cause
**Problem:** Multiple warnings appeared but needed to identify if they were system-wide or isolated.

**Solution:** Correlated warnings with IP addresses, discovered all memory issues came from single source (192.168.1.104).

## Future Enhancements

### Planned Improvements

**1. Acceleration Detection**
- Detect not just IF metrics increase, but if rate of increase is accelerating
- Critical for distinguishing normal load vs. memory leaks
- Enables predictive failure alerting

**2. Configurable Thresholds**
- Allow users to define what counts as "high" error rate
- Configurable alert levels (warning vs. critical)
- Config file for customization

**3. Multi-Format Log Support**
- Currently optimized for space-delimited logs
- Add support for JSON logs, CSV logs
- Automatic format detection

**4. HTML Report Generation**
- Generate visual HTML reports with charts
- Email-friendly formatting
- Historical trend graphs

**5. Real-Time Monitoring Mode**
- `tail -f` integration for live log monitoring
- Continuous analysis with alerts
- Dashboard display

These enhancements demonstrate understanding of production requirements and scalability thinking.

## Project Files
- **Script:** `../../scripts/bash/analyze_log.sh`
- **Sample Log:** `../../logs/server.log`
- **Sample Report:** `../../logs/report.txt`
- **Commands Reference:** `commands.txt`
- **Learning Notes:** `Learnings.md`


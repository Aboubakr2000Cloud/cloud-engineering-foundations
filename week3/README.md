# Week 3: Network Troubleshooting Toolkit

## Overview
Automated network diagnostics script that checks connectivity, DNS resolution, routing, web access, and port status for any host.

## Project Structure
```bash
week3/
├── netcheck.sh             # Main diagnostics script 
├── network_report.txt      # Generated report
├── commands.txt            # Command reference
├── Learnings.md            # Learning Notes
└── README.md               # This file
```

## Features
- Multi-host support
- Color-coded output
- Timestamped reports
- Timeout handling
- Port scanning
- Summary analysis

## Usage
```bash
cd scripts/bash
chmod +x scripts/bash/netcheck.sh
./netcheck.sh google.com
./netcheck.sh google.com github.com amazon.com
cat logs/network_report_2025-10-30_02-02-42.txt
```

## What It Checks
1. Ping connectivity
2. DNS resolution
3. Network route tracing
4. HTTP/HTTPS status
5. Local listening ports
6. Specific port availability

## Skills Demonstrated
- Bash scripting with functions
- Network troubleshooting commands
- Error handling and timeouts
- Multiple host processing
- Report generation
- Professional output formatting

## Project Files
- **Script:** `../../scripts/bash/netcheck.sh`
- **Sample Report:** `../../logs/network_report_2025-10-30_02-02-42.txt`
- **Commands Reference:** `../../docs/week3/commands.txt`
- **Learning Notes:** `../../docs/week3/Learnings.md`
- **Project Readme:** `../../docs/week3/README.md`

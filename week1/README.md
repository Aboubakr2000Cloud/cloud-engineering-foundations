# Week 1: Linux Fundamentals
## Focus:
- Bash scripting basics  
- Configuration file integration  
- System information commands
## Overview
This first project introduced the core principles of Linux scripting and automation.  
The goal was to create a simple yet functional system information script that reads parameters from a configuration file and prints customized system details dynamically.
## Project Structure

```
cloud-learning-project/     
├── configs/                 
│ └── system.conf           # Configuration file  
└── scripts/
  └── system_info.sh        # Main script
``` 
- system_info.sh: The main bash script that prints system information.  
- system.conf: A configuration file that stores environment variables and user preferences.
## Script Explanation
The script sources (source) the configuration file, dynamically loading variables defined there.  
Depending on the configuration values, it conditionally displays system information such as the current date, the active user, and disk space usage.
## Tools & Commands Used
- Bash — scripting language and shell interpreter  
- chmod — set file permissions  
- df, date, whoami — retrieve system information  
- source — import external configuration variables  
## Usage:
- Clone this repository
- Navigate to project : cd cloud-learning-project 
- Make script executable: chmod +x scripts/bash/system_info.sh
- Run the script: ./scripts/bash/system_info.sh
- Modify settings to change output in: configs/system.conf
 ## Skills Demonstrated
- Bash scripting fundamentals  
- Using configuration files for modular scripts
- Command substitution and variable handling
- File permissions and script execution management (chmod +x)
- Understanding standard Linux commands (date, whoami, df)

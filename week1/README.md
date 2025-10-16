# Week 1: Linux Fundamentals
## Focus:
Bash scripting basics  
Configuration file integration  
System information commands
## Project Overview
This first project introduced the core principles of Linux scripting and automation.  
The goal was to create a simple yet functional system information script that reads parameters from a configuration file and prints customized system details dynamically.
## Script Structure

cloud-learning-project/  
├── configs/  
│ └── system.conf  
└── scripts/  
    └── system_info.sh  
```
project/
├── configs/
│ └── system.conf
└── scripts/
  └── system_info.sh
```
  
    system_info.sh: The main bash script that prints system information.  
    system.conf: A configuration file that stores environment variables and user preferences.
## Script Explanation
The script sources (source) the configuration file, dynamically loading variables defined there.
Depending on the configuration values, it conditionally displays system information such as the current date, the active user, and disk space usage.

## How To Execute The Script:
1/ Clone this repository
 2/ Navigate to project : cd cloud-learning-project 
 3/ Make script executable: chmod +x scripts/bash/system_info.sh
 4/ Run the script: ./scripts/bash/system_info.sh
### 5/ Modify settings to change output in: configs/system.conf

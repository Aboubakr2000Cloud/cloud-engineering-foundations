# Week 1: Linux Fundamentals
## Focus:
- Bash scripting basics  
- Configuration file integration  
- System information commands
## Overview
This first project introduced the core principles of Linux scripting and automation.  
The goal was to create a simple yet functional system information script that reads parameters from a configuration file and prints customized system details dynamically.
## Project Structure

```bash
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
## Quick Start:
From repository root:
```bash
./scripts/bash/system_info.sh
```
 ## Skills Demonstrated
- Bash scripting fundamentals  
- Using configuration files for modular scripts
- Command substitution and variable handling
- File permissions and script execution management (chmod +x)
- Understanding standard Linux commands (date, whoami, df)
## Sample Output
```bash
Welcome_to_my_system!
current date: Thu Oct 16 03:08:27 AM +01 2025
current user: abou
disk space: Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2        22G   12G  9.3G  56% /

```
## Challenges & Solutions
### Challenge 1: 
**Problem:** Understanding what bash actually is and how it executes commands.

**Solution:** Studied how shell interpreters work and practiced small commands manually before scripting.

### Challenge 2: 
**Problem:** Linking the script with an external config file.

**Solution:** Learned to use the "source" command to import variables from another file.

### Challenge 3: 
**Problem:** Keeping the script flexible for repeated runs.

**Solution:** Used variables (SHOW_DATE, SHOW_USER, SHOW_DISK) in the config file instead of hardcoding.  

### Challenge 4: 
**Problem:** Debugging permission issues.

**Solution:** Used "chmod +x" to make the script executable.  

### Challenge 5: 
**Problem:** Ensuring clear output formatting.

**Solution:** Added "echo" commands and clean output messages.

## Learning Outcome
This project built a strong foundation in automation and configuration management.  
It showed how even a small script can adapt to user preferences, setting the stage for more advanced bash projects and system automation tasks in later weeks.

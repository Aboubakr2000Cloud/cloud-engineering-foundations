# Week 4 — Bash Scripting & Crontab: Complete Learning Journey

## Core Bash Scripting Concepts

### Variables & Data Types
- **Variable assignment**: No spaces around `=` → `NAME="value"`
- **Variable expansion**: Use `$VAR` or `${VAR}` for clarity
- **Special variables**: 
  - `$0`: Script name
  - `$1, $2, ...`: Command-line arguments
  - `$#`: Number of arguments
  - `$?`: Exit code of last command

### Control Flow

#### If Statements
```bash
if [ condition ]; then
    # commands
elif [ condition ]; then
    # commands
else
    # commands
fi
```

**Important lessons learned:**
- Use `elif` instead of nested `if-else` for cleaner code
- Comparison operators:
  - Numbers: `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`
  - Strings: `=`, `!=`
- Logical operators: `-a` (AND), `-o` (OR)
- `[ "$VAR" -eq 000 ]` checks numeric equality

#### Case Statements
```bash
case "$1" in
    option1)
        # commands
        ;;
    option2)
        # commands
        ;;
    *)
        # default case
        ;;
esac
```

**Key insight**: Perfect for command-line argument handling (check, report, status, help)

#### Loops
```bash
# While loop with IFS
while IFS=',' read -r url name max_time; do
    # Process each line
done < input_file
```

**Critical learning**: `IFS=','` sets field separator for parsing CSV data

### Functions
```bash
function_name() {
    # function body
    local VAR="value"  # Local variable
    return 0           # Exit code
}
```

**Best practices learned:**
- Use functions for modularity and reusability
- One function = one responsibility
- Variables inside functions can be `local` to avoid conflicts

### Exit Codes & Error Handling
- `exit 0`: Success
- `exit 1`: General error
- `curl` returns `000` for connection failures
- Always check if operations succeeded before proceeding

## Text Processing Mastery

### grep: Pattern Matching
```bash
grep "pattern" file              # Basic search
grep -c "pattern" file           # Count matches
grep -E "pat1|pat2|pat3" file   # Extended regex (OR logic)
grep -v "pattern" file           # Invert match (exclude)
grep -o "pattern" file           # Only matching part
```

**Real-world application**: Filtering logs by date, status, or site name

### awk: Field Processing
```bash
# Print specific columns
awk '{print $3}'

# Pattern matching
awk '/pattern/ {print $1}'

# Calculations
awk '{sum += $1; count++} END {print sum/count}'

# Multi-line awk with loops
awk '{
    for(i=1; i<=NF; i++) {
        if($i ~ /[0-9]+ms/) {
            # Process matching field
        }
    }
}'
```

**Key lessons:**
- `$1, $2, $3...`: Field numbers (columns)
- `NF`: Number of fields in current line
- `END`: Execute after processing all lines
- Use `gsub()` for text replacement within awk
- Single vs double quotes matter for variable expansion

### sed: Stream Editor
```bash
sed 's/pattern/replacement/'     # Substitute
sed 's/ms//'                     # Remove text
sed 's/\x1b\[[0-9;]*m//g'       # Remove ANSI color codes
```

**Critical discovery**: Color codes in log files break sorting—strip them before processing!

### cut: Column Extraction
```bash
cut -d',' -f1              # First field, comma-delimited
cut -d']' -f2              # Split by ], take second part
```

**Use case**: Quick field extraction from structured data

### sort: Ordering Data
```bash
sort -n                    # Numeric sort
sort -r                    # Reverse order
sort -rn                   # Reverse numeric
sort -k1 -rn              # Sort by column 1, reverse numeric
sort -u                    # Unique values only
```

**Gotcha learned**: Text sort vs numeric sort—"100" comes before "20" in text sort!

### Other Utilities
- `tail -n N`: Last N lines
- `tail -f`: Follow file in real-time (perfect for monitoring)
- `head -n N`: First N lines
- `wc -l`: Count lines

## Working with curl

### Basic Health Checking
```bash
# Get HTTP status code
curl -I -s -o /dev/null -w "%{http_code}" "$url"

# Get response time
curl -o /dev/null -s -w "%{time_total}" "$url"

# Get both in one request
curl -o /dev/null -s -w "%{http_code},%{time_total}" "$url"
```

**Flags explained:**
- `-I`: HEAD request (faster, no body)
- `-s`: Silent mode (no progress bar)
- `-o /dev/null`: Discard output
- `-w`: Custom output format
- `--max-time 10`: Timeout after 10 seconds

**Critical insight**: Always set timeouts to prevent hanging on unresponsive sites

### curl Output Variables
- `%{http_code}`: HTTP status (200, 404, etc.)
- `%{time_total}`: Total time in seconds
- `%{time_connect}`: Connection establishment time

## Date & Time Handling

### date Command
```bash
date +%F                   # 2025-11-15 (YYYY-MM-DD)
date '+%F %H:%M:%S'        # 2025-11-15 14:30:45
date +%s                   # Unix timestamp
```

**Use cases:**
- Log timestamps: `[$(date '+%F %H:%M:%S')]`
- Report filenames: `report_$(date +%F).txt`
- Filtering logs by today: `grep "$(date +%F)" log_file`

## File Operations

### Reading Files
```bash
# Line by line with while
while read -r line; do
    echo "$line"
done < file

# With custom delimiter
while IFS=',' read -r col1 col2 col3; do
    echo "$col1"
done < file.csv
```

### Writing Files
```bash
echo "text" > file         # Overwrite
echo "text" >> file        # Append

# Block redirection
{
    echo "line 1"
    echo "line 2"
} > output_file
```

**Important distinction:**
- `>`: Creates new file or overwrites
- `>>`: Appends to existing file

### Path Handling
**Relative vs Absolute paths:**
- Relative: `configs/file.conf` (depends on current directory)
- Absolute: `/home/user/project/configs/file.conf` (works from anywhere)

**Critical learning**: Cron jobs need absolute paths or must `cd` to the right directory first!

**Path navigation:**
- `../`: Up one level
- `../../`: Up two levels
- Always start absolute paths with `/`

## Cron Scheduling

### Cron Syntax
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Common Patterns
```bash
*/5 * * * *        # Every 5 minutes
0 * * * *          # Every hour (at minute 0)
0 0 * * *          # Daily at midnight
0 9 * * 1-5        # Weekdays at 9 AM
* * * * *          # Every minute (testing only!)
```

### Cron Management
```bash
crontab -e         # Edit cron jobs
crontab -l         # List current jobs
crontab -r         # Remove all jobs
```

### Cron Best Practices Learned

1. **Use absolute paths**: `/full/path/to/script.sh`
2. **Change directory first**: `cd /path && ./script.sh`
3. **Redirect output for debugging**: `command >> /tmp/cron.log 2>&1`
4. **Test manually first**: Run the exact command before scheduling
5. **Start with frequent testing**: Use `* * * * *` (every minute) to verify it works, then change to real schedule

### Cron Debugging
- Check syslog: `grep CRON /var/log/syslog`
- Verify script is executable: `ls -l script.sh` (should show `-rwxr-xr-x`)
- Test the exact cron command manually
- Add error logging: `command 2>&1 >> /tmp/error.log`

## Data Processing & Analysis

### Calculating Statistics

**Success Rate:**
```bash
SUCCESS_TOTAL=$(grep "SUCCESS" log | wc -l)
TOTAL=$(wc -l < log)
SUCCESS_RATE=$((SUCCESS_TOTAL * 100 / TOTAL))
```

**Average Response Time:**
```bash
AVG=$(grep -o '[0-9]\+ms' log | sed 's/ms//' | \
      awk '{sum += $1; count++} END {print int(sum/count)}')
```

**Finding Top N:**
```bash
# Sort and get top 3
sort -rn | head -3
```

### Integer Math in Bash
```bash
RESULT=$((5 + 3))              # Addition
RESULT=$((10 * 100 / 3))       # Multiply then divide (for percentages)
RESULT=$((SUCCESS * 100 / TOTAL))  # Success rate calculation
```

**Important**: Bash only does integer math—no decimals! Multiply by 100 before dividing for percentages.

## Color Formatting

### ANSI Color Codes
```bash
RED="\e[31m"
GREEN="\e[32m"
RESET="\e[0m"

echo -e "${GREEN}Success${RESET}"
```

**Critical lessons learned:**

1. **Don't use colors in log files!**
   - Color codes break sorting and parsing
   - Store plain text in logs
   - Use colors only for terminal output

2. **With `-e` flag**: `echo -e` interprets escape codes
3. **Without `-e` flag**: `echo` writes literal `\e[32m` text
4. **Strip colors from logs**: `sed 's/\x1b\[[0-9;]*m//g'`

## Problem-Solving Lessons

### Race Conditions
**Problem**: Reading log file while script is writing to it causes mixed data.

**Solution**: 
- Use timestamps to filter complete cycles
- Get last entry per site individually
- Don't rely on "last N lines" during active writing

### Variable Scope Issues
**Problem**: Using `{ } > file` caused variables to disappear.

**Solution**: Redirect individual `echo` statements, not entire blocks.

### Sorting Failures
**Problem**: Numbers sorting incorrectly (581 before 3915).

**Solution**: 
- Ensure clean numeric data (no color codes)
- Use `-n` flag for numeric sort
- Specify sort column: `sort -k1 -rn`

### Bracket Syntax
**Problem**: `$RESPONSE_TIMEms` looked for variable `RESPONSE_TIMEms` instead of `RESPONSE_TIME` + "ms".

**Solution**: Use `${RESPONSE_TIME}ms` to clearly separate variable from text.

## Professional Script Design

### Script Structure
```bash
#!/bin/bash

# Configuration section
VAR="value"

# Functions
function1() { }
function2() { }

# Main logic
case "$1" in
    command1) function1 ;;
    command2) function2 ;;
    *) show_help; exit 1 ;;
esac
```

### User Experience
- **Provide feedback**: Tell users where files are saved
- **Show usage**: `--help` command with examples
- **Handle errors gracefully**: Don't just fail silently
- **Use clear messages**: "✓ Success!" or "✗ Error: ..."

### Code Organization
- **Functions for reusability**: Don't repeat code
- **Configuration at top**: Easy to modify
- **Comments for clarity**: Explain complex logic
- **Consistent naming**: `snake_case` for bash functions/variables

## Key Takeaways

### Technical Skills Gained
1. **Bash scripting fluency**: Variables, functions, control flow
2. **Text processing pipeline**: grep → awk → sed → sort
3. **System automation**: Cron scheduling and log management
4. **Data analysis**: Calculating statistics from raw logs
5. **Error handling**: Detecting and logging failures

### Problem-Solving Approaches
1. **Debug incrementally**: Test each command in the pipeline separately
2. **Use absolute paths**: Avoid environment-dependent issues
3. **Test manually first**: Verify before automating
4. **Keep data clean**: Separate display formatting from storage
5. **Handle edge cases**: Connection timeouts, missing files, division by zero

### Real-World Applications
- **Website monitoring**: Production uptime tracking
- **Log analysis**: Extract insights from system logs
- **Automated reporting**: Daily/weekly status summaries
- **Alert systems**: Detect and notify on failures
- **Performance tracking**: Response time trends

---

## Looking Forward

This week built a strong foundation in:
- **Scripting for automation** (essential for DevOps)
- **Log analysis** (critical for troubleshooting)
- **System monitoring** (real-world production skill)

These skills directly apply to:
- Week 8: Automation & Integrations
- Week 19: CI/CD pipelines
- Week 20: CloudWatch & Monitoring

**Next**: Week 5 starts Python, which will complement bash for more complex automation tasks!

# Week 5 — Python Fundamentals

## Overview
Week 5 introduces Python programming, covering core language fundamentals including data types, control flow, functions, and modules. The capstone project is a feature-rich command-line calculator demonstrating Python's capabilities for building interactive applications.

## Project: CLI Calculator
A comprehensive calculator application with advanced mathematical operations, memory functions, calculation history, and persistent storage. The calculator provides an interactive menu-driven interface with error handling and user-friendly output.

### Project Structure

```
cloud-learning-project/
├── scripts/
│   └── python/
│        └── calculator.py      # Main calculator application
└── logs/                
    └── calc_history.txt        # Calculation history (auto-generated)
```

## Features

### Basic Operations
- Addition, Subtraction, Multiplication, Division
- Modulus: Remainder of division
- Power: Exponentiation (a^b)

### Advanced Mathematics
- Square Root: With negative number validation
- Trigonometry: Sin, Cos, Tan (degree-based)
- Logarithms: Natural log (ln) and base-10 log

### Memory Functions
- Store Result: Save calculation result to memory
- Recall Memory: Use stored value in calculations
- Clear Memory: Reset memory storage
- Memory Integration: Use 'M' in any input to recall memory

### History & Persistence
- Calculation History: Track all operations in current session
- Show Last 5: Display recent calculations
- Clear History: Reset history for new session
- File Export: Save complete history to calc_history.txt on exit

### User Experience
- Color-Coded Output: Green for results, red for errors
- Error Handling: Graceful handling of:
  - Division by zero
  - Negative square roots
  - Invalid number inputs

- Interactive Menu: Clear numbered options
- Input Validation: Ensures valid numeric input

## Usage
### Commands

```
# make the calculator executable:
chmod +x scripts/python/calculator.py
# run the calculator:
python3 scripts/python/calculator.py

```
### Example Session
=== Calculator Menu ===
1. Addition
2. Subtraction
...
Choose an operation: 1

Enter first number: 10
Enter second number: 5
10.0 + 5.0 = 15.0

Choose an operation: 13
Stored 15.0 in memory

Choose an operation: 6
Enter first number: M
Enter second number: 2
15.0 ** 2.0 = 225.0

### Memory Feature
When prompted for a number, type M to use the last stored result:
Enter first number: M    # Uses memory value

### History Export
On exit, all calculations are automatically saved to calc_history.txt:
10.0 + 5.0 = 15.0
15.0 ** 2.0 = 225.0
...

## What It Does
1. Interactive Calculator: Presents menu-driven interface for selecting operations
2. Performs Calculations: Executes mathematical operations with proper error handling
3. Manages Memory: Stores and recalls results for chained calculations
4. Tracks History: Maintains session log of all calculations
5. Validates Input: Ensures valid numeric input with helpful error messages
6. Persists Data: Saves calculation history to file on exit

## Skills Demonstrated

### Python Fundamentals
✅ Variables and data types (int, float, string)
✅ Functions with parameters and return values
✅ Control flow (if/elif/else, while loops)
✅ Exception handling (try/except)
✅ String formatting (f-strings)
✅ User input and type conversion

### Modules & Imports
✅ Using standard library modules (math)
✅ Importing specific functions
✅ Module organization and structure

### Data Structures
✅ Lists for storing history
✅ List methods (append, clear, slicing)
✅ Iterating over lists

### File Operations
✅ Writing to files
✅ Context managers (with statement)
✅ File I/O for data persistence

### Error Handling
✅ Try/except blocks
✅ Specific exception types (ZeroDivisionError, ValueError)
✅ Graceful error messages
✅ Input validation loops

### Code Organization
✅ Function decomposition
✅ Docstrings for documentation
✅ Main function pattern
✅ if __name__ == "__main__" idiom

## Project Files
- calculator.py
Main application file containing:

Operation Functions: Mathematical operations (add, subtract, multiply, divide, modulus, power, square_root, sin, cos, tan, log, log10)
Utility Functions:

get_number(): Input handler with memory integration and validation
show_menu(): Display operation options
show_history(): Display calculation history


Main Function: Interactive loop managing user flow and state
File Export: Saves history on program exit

- calc_history.txt
Auto-generated file storing all calculations from the session in human-readable format.

## Technical Highlights

### Memory System
Implemented persistent memory across calculations:
```
memory = result           # Store
a = get_number("...", memory)  # Recall in any input
```

### Error Handling Pattern
Comprehensive exception handling for mathematical edge cases:
```
try:
    return a / b
except ZeroDivisionError:
    print(RED + "Error: Cannot divide by zero!" + RESET)
    return None
```

### History Management
Dynamic list with display limiting:
```
history.append(calc)              # Add to history
for calc in history[-5:]:         # Show last 5
    print(calc)    
```    
    
### Color-Coded Output

ANSI escape codes for enhanced user experience:

```
GREEN = "\033[92m"
print(GREEN + calc + RESET)
```

**Week 5 Complete!** This project demonstrates solid Python fundamentals including functions, error handling, file I/O, and interactive application development—essential skills for automation and scripting in cloud engineering.

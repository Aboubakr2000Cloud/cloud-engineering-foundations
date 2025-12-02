# Week 5 — Python Fundamentals: Key Learnings

## Python Basics

### Variables & Data Types
```python
# No type declaration needed
name = "Alice"          # string
age = 25                # int
height = 5.9            # float
is_student = True       # boolean

# Type conversion
num_str = "42"
num_int = int(num_str)  # Convert to integer
```

### String Formatting
```python
# f-strings (modern, preferred)
name = "Alice"
age = 25
print(f"{name} is {age} years old")
print(f"Result: {10 + 5}")

# Format specifiers
price = 19.99
print(f"Price: ${price:.2f}")  # 2 decimal places
```

### User Input
```python
# Get input (always returns string)
name = input("Enter your name: ")

# Convert to number
age = int(input("Enter age: "))
price = float(input("Enter price: "))
```

## Lists & Comprehensions

### Lists
```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Accessing
numbers[0]      # First: 1
numbers[-1]     # Last: 5
numbers[1:3]    # Slice: [2, 3]

# Modifying
numbers.append(6)       # Add to end
numbers.pop()           # Remove last
numbers.remove(3)       # Remove value
len(numbers)            # Length
```

### List Comprehensions
```python
# Create list from range
squares = [x**2 for x in range(1, 6)]
# Result: [1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(10) if x % 2 == 0]
# Result: [0, 2, 4, 6, 8]

# Transform
words = ["hello", "world"]
upper = [w.upper() for w in words]
# Result: ['HELLO', 'WORLD']
```

## Control Flow

### If/Elif/Else
```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")

# One-liner (ternary)
status = "Pass" if score >= 60 else "Fail"
```

### Loops
```python
# For loop
for i in range(5):      # 0 to 4
    print(i)

# Loop through list
for item in my_list:
    print(item)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
break       # Exit loop
continue    # Skip to next iteration
```

## Functions

### Basic Functions
```python
def greet(name):
    """Function with parameter"""
    return f"Hello, {name}!"

result = greet("Alice")
```

### Multiple Parameters
```python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        return None  # Handle edge case
    return a / b
```

### Default Parameters
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")              # Uses default
greet("Bob", "Hi")          # Custom greeting
```

### Docstrings
```python
def calculate(a, b):
    """
    Calculate sum of two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    return a + b
```

## Modules & Imports

### Importing Modules
```python
# Import entire module
import math
result = math.sqrt(16)

# Import specific functions
from math import sqrt, sin, cos
result = sqrt(16)

# Import with alias
import math as m
result = m.sqrt(16)
```

### Common Math Functions
```python
import math

math.sqrt(16)           # Square root: 4.0
math.pow(2, 3)          # Power: 8.0
math.sin(math.pi/2)     # Sin: 1.0
math.cos(0)             # Cos: 1.0
math.log(10)            # Natural log
math.log10(100)         # Base-10 log: 2.0
math.radians(180)       # Convert degrees to radians
```

## Error Handling

### Try/Except
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Multiple Exceptions
```python
try:
    num = int(input("Enter number: "))
    result = 10 / num
except ValueError:
    print("Invalid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Input Validation Loop
```python
while True:
    try:
        num = int(input("Enter a number: "))
        break  # Exit loop if successful
    except ValueError:
        print("Invalid! Try again.")
```

## File Operations

### Writing to Files
```python
# Write mode (overwrites)
with open("data.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# Append mode
with open("data.txt", "a") as f:
    f.write("Additional line\n")
```

### Reading from Files
```python
# Read entire file
with open("data.txt", "r") as f:
    content = f.read()
    print(content)

# Read line by line
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())
```

### Context Managers
```python
# Good practice - automatically closes file
with open("file.txt", "w") as f:
    f.write("content")
# File is automatically closed after this block
```

## Key Patterns from Calculator Project

### Menu System
```python
while True:
    show_menu()
    choice = input("Choose: ")
    
    if choice == '0':
        break  # Exit
    elif choice == '1':
        # Handle operation
    else:
        print("Invalid choice!")
```

### State Management
```python
# Maintain state across loop iterations
history = []
memory = None

# Update state
history.append(calculation)
memory = result
```

### Input with Validation
```python
def get_number(prompt, memory=None):
    """Get validated number with memory support"""
    while True:
        user_input = input(prompt)
        if user_input.upper() == 'M' and memory is not None:
            return memory
        try:
            return float(user_input)
        except ValueError:
            print("Invalid number!")
```

### Color Output
```python
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

print(GREEN + "Success!" + RESET)
print(RED + "Error!" + RESET)
```

## Python vs C: Key Differences

| Feature | C | Python |
|---------|---|--------|
| **Variables** | `int x = 5;` | `x = 5` |
| **Functions** | `int add(int a, int b) { }` | `def add(a, b):` |
| **Arrays/Lists** | `int arr[5];` | `arr = [1,2,3,4,5]` |
| **Strings** | `char str[] = "hello";` | `str = "hello"` |
| **Print** | `printf("%d", x);` | `print(x)` |
| **Input** | `scanf("%d", &x);` | `x = int(input())` |
| **Memory** | Manual allocation | Automatic |
| **Type** | Static (declared) | Dynamic (inferred) |

## Best Practices Learned

### Code Organization
1. **Functions for reusability**: Break code into logical functions
2. **Docstrings**: Document what functions do
3. **Main function pattern**: Use `if __name__ == "__main__":`
4. **Meaningful names**: `calculate_total()` not `calc()`

### Error Handling
1. **Always validate input**: Use try/except for conversions
2. **Handle edge cases**: Division by zero, negative square roots
3. **Provide helpful messages**: Tell user what went wrong

### User Experience
1. **Clear prompts**: "Enter first number:" not "Number?"
2. **Feedback**: Confirm actions ("Stored 15.0 in memory")
3. **Color coding**: Green for success, red for errors
4. **Input flexibility**: Allow 'M' for memory recall

## Common Pitfalls & Solutions

### Indentation Errors
**Problem**: Python uses indentation for blocks
```python
# Wrong
if x > 5:
print("Big")  # IndentationError

# Right
if x > 5:
    print("Big")
```

### Undefined Variables
**Problem**: Using variable before assignment
```python
# Wrong
memory = result  # result might not exist

# Right
if 'result' in locals():
    memory = result
```

### Integer Division
**Problem**: `/` always returns float in Python 3
```python
10 / 3      # 3.3333... (float)
10 // 3     # 3 (integer division)
```

### String Concatenation
**Problem**: Can't mix strings and numbers
```python
# Wrong
"Result: " + 42  # TypeError

# Right
"Result: " + str(42)
f"Result: {42}"
```

## Key Takeaways

### Technical Skills
- ✅ Python syntax and structure
- ✅ Functions and modular code
- ✅ Error handling patterns
- ✅ File I/O operations
- ✅ Working with modules

### Problem-Solving
- ✅ Breaking complex problems into functions
- ✅ Input validation and error handling
- ✅ State management across iterations
- ✅ User experience considerations

### Real-World Applications
- **CLI tools**: Interactive command-line applications
- **Automation scripts**: Tasks requiring user interaction
- **Data processing**: Reading/writing files, calculations
- **Prototyping**: Quick tool development

---

**Next Steps**: Week 6 covers Python data structures (dictionaries, sets, tuples) and file I/O for more complex automation tasks!

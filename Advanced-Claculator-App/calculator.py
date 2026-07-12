#!/usr/bin/env python3
"""
Week 5 Project: CLI Calculator
Interactive calculator with history
"""
import math
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# ===== OPERATION FUNCTIONS =====

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply a with b"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    try:
        return a / b
    except ZeroDivisionError:
        print(RED + "Error: Cannot divide by zero!" + RESET)
        return None

def modulus(a, b):
    """Modulus of a and b"""
    try:
        return a % b
    except ZeroDivisionError:
        print(RED + "Error: Cannot divide by zero!" + RESET)
        return None

def power(a, b):
    """Raising a to the power of b"""
    return a ** b

def square_root(a):
    """Square root a"""
    try:
        return math.sqrt(a)
    except ValueError:
        print(RED + "Cannot take square root of a negative number!" + RESET)
        return None

def sin(a):
    """Sin"""
    return math.sin(math.radians(a))

def cos(a):
    """Cos"""
    return math.cos(math.radians(a))

def tan(a):
    """Tan"""
    return math.tan(math.radians(a))

def log(a):
    """Log """
    return math.log(a)

def log10(a):
    """Log10 """
    return math.log10(a) 

# ===== UTILITY FUNCTIONS =====

def get_number(prompt, memory=None):
    while True:
        user_input = input(prompt + " (or type 'M' for memory): ")
        if user_input.upper() == 'M' and memory is not None:
            return memory
        try:
            return float(user_input)
        except ValueError:
            print(RED + "Invalid number! Try again." + RESET)

def show_menu():
    print()
    print("=== Calculator Menu ===")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Power")
    print("7. Square_root")
    print("8. Cos")
    print("9. Sin")
    print("10. Tan")
    print("11. Log")   
    print("12. Log10")
    print("13. Store result in memory")
    print("14. Recall memory")
    print("15. Clear memory")
    print("16. Show History")
    print("17. Clear History")
    print("0. Exit")

def show_history(history):
    """Display calculation history"""
    print("\n=== Calculation History ===")
    for calc in history[-5:]: 
        print(calc)
# ===== MAIN PROGRAM =====

def main():
    """Main calculator loop"""
    print("=== Welcome to CLI Calculator ===")
    history = []
    memory = None  
 
    while True:
        show_menu()
        choice = input("\nChoose an operation: ")
        
        if choice == '0':
            print("\nThank you for using Calculator!")
            break
        elif choice == '1':                  
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = add(a, b)
            calc = (f"{a} + {b} = {result}")
            print(GREEN + calc + RESET)  
            history.append(calc)
        elif choice == '2':
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = subtract(a, b)
            calc = (f"{a} - {b} = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '3':
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = multiply(a, b)
            calc = (f"{a} * {b} = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '4':
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = divide(a, b)
            calc = (f"{a} / {b} = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '5':
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = modulus(a, b)
            calc = (f"{a} % {b} = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '6':
            a = get_number("Enter first number: ", memory)
            b = get_number("Enter second number: ", memory)
            result = power(a, b)
            calc = (f"{a} ** {b} = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '7':
            a = get_number("Enter a number: ", memory)
            result = square_root(a) 
            calc = (f"square({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '8':
            a = get_number("Enter a number: ", memory)
            result = cos(a)
            calc = (f"cos({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '9':
            a = get_number("Enter a number: ", memory)
            result = sin(a)
            calc = (f"sin({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '10':
            a = get_number("Enter a number: ", memory)
            result = tan(a)
            calc = (f"tan({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '11':
            a = get_number("Enter a number: ", memory)
            result = log(a)
            calc = (f"log({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '12':
            a = get_number("Enter a number: ", memory)
            result = log10(a)
            calc = (f"log10({a}) = {result}")
            print(GREEN + calc + RESET)
            history.append(calc)
        elif choice == '13':   
            if 'result' in locals() and result is not None:
               memory = result
               print(f"Stored {memory} in memory")
            else:
               print(RED + "No result to store! Perform a calculation first." + RESET)
        elif choice == '14':  
            if memory is not None:
               print(f"Recalled {memory} from memory")
               a = memory  
            else:
                print("Memory is empty")
        elif choice == '15':  
            memory = None
            print("Memory cleared")
        elif choice == '16':
            show_history(history)
        elif choice == '17':
            history.clear()
        else:
            print(RED + "Invalid choice! Please try again." + RESET)
    with open("/home/abou/cloud-learning-project/logs/calc_history.txt", "a") as f:
        for item in history:
            f.write(item + "\n")
   
if __name__ == "__main__":
    main()


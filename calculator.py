def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

def calculator():
    while True:
        print("----- Simple Calculator ------")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        try:
            choice = int(input("Enter choice (1/2/3/4/5): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 5:
            print("\n\nThank You for using!")
            break

        if choice not in [1, 2, 3, 4]:
            print("Invalid choice. Please enter a valid option.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

        if choice == 1:
            result = add(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif choice == 2:
            result = subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif choice == 3:
            result = multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif choice == 4:
            result = divide(num1, num2)
            print(f"{num1} / {num2} = {result}")

        try:
            another_calculation = input("Do you want to perform another calculation? (yes/no): ").lower()
        except ValueError:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue

        if another_calculation != 'yes':
            print("\nThank You for using!")
            break

if __name__ == "__main__":
    calculator()

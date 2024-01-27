import secrets
import string

WEAK = 'weak'
AVERAGE = 'average'
STRONG = 'strong'

def generate_password(length, complexity):
    characters = get_complexity_characters(complexity)
    
    if complexity == STRONG:
        first_char = secrets.choice(string.ascii_letters)
        rest_of_password = ''.join(secrets.choice(characters) for _ in range(length - 2))
        password = first_char + rest_of_password + secrets.choice(string.digits) + secrets.choice(string.punctuation)
    elif complexity == AVERAGE:
        first_char = secrets.choice(string.ascii_letters)
        rest_of_password = ''.join(secrets.choice(characters) for _ in range(length - 1))
        password = first_char + rest_of_password + secrets.choice(string.digits)
    elif complexity == WEAK:
        password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password

def get_complexity_characters(complexity):
    if complexity == WEAK:
        return string.ascii_letters
    elif complexity == AVERAGE:
        return string.ascii_letters + string.digits
    elif complexity == STRONG:
        return string.ascii_letters + string.digits + string.punctuation
    else:
        print("Invalid complexity. Please enter 'weak', 'average', or 'strong'.")
        return None

def validate_length(length, complexity):
    if complexity == WEAK and length < 4:
        print(f"Password length must be at least 4 for {WEAK} complexity.")
        return False
    elif complexity == AVERAGE and length < 6:
        print(f"Password length must be at least 6 for {AVERAGE} complexity.")
        return False
    elif complexity == STRONG and length < 8:
        print(f"Password length must be at least 8 for {STRONG} complexity.")
        return False
    return True

def main():
    print("------- Welcome to the Password Generator -------")

    while True:
        length = int(input("\nEnter the desired password length: "))
        complexity = input("Enter the desired password complexity (weak/average/strong): ")

        while complexity not in [WEAK, AVERAGE, STRONG]:
            print("Invalid complexity. Please enter 'weak', 'average', or 'strong'.")
            complexity = input("\nEnter the desired password complexity (weak/average/strong): ")

        if not validate_length(length, complexity):
            continue

        password = generate_password(length, complexity)
        print("\nGenerated Password:", password)

        generate_again = input("\nDo you want to generate another password? (yes/no): ")
        if generate_again.lower() != 'yes':
            print("\n\nThank you for using the Password Generator!")
            break

if __name__ == '__main__':
    main()

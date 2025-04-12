import itertools

# Function to calculate the number of case combinations (uppercase and lowercase)
def calculate_case_combinations(s):
    return 2 ** len(s)  # Each character has 2 possibilities (uppercase and lowercase)

# Function to calculate the number of number combinations (normal and reversed)
def calculate_number_combinations(nums):
    return 2  # Two combinations for numbers: normal and reversed

# Function to calculate the total number of combinations
def calculate_total_combinations(word, numbers):
    case_combinations = calculate_case_combinations(word)
    number_combinations = calculate_number_combinations(numbers)
    total_combinations = case_combinations * number_combinations * 2  # Word+Number and Number+Word
    return total_combinations

# Generate all case combinations (uppercase and lowercase)
def generate_case_combinations(s):
    return [''.join(x) for x in itertools.product(*[(c.lower(), c.upper()) for c in s])]

# Generate number combinations (normal and reversed order)
def generate_number_combinations(nums):
    return [nums, nums[::-1]]  # Normal and reversed order

# Generate all possible password combinations
def generate_password_combinations(word, numbers):
    word_combinations = generate_case_combinations(word)
    number_combinations = generate_number_combinations(numbers)

    all_combinations = []

    for wc in word_combinations:
        for nc in number_combinations:
            all_combinations.append(wc + nc)  # word + number                           all_combinations.append(nc + wc)  # number + word

    return all_combinations

# Asking for user input
word = input("Please enter your username: ")
numbers = input("Please enter your birth year (optional): ")

# If no birth year is provided, use a default value
if not numbers:
    numbers = "1345"  # Default birth year

# Calculate the total number of combinations
total_combinations = calculate_total_combinations(word, numbers)
print(f"Total possible combinations: {total_combinations}")

# Generate the password list
password_list = generate_password_combinations(word, numbers)

# Save the passwords to a file
with open("password_list.txt", "w") as file:
    for password in password_list:
        file.write(password + "\n")

print(f"{len(password_list)} passwords have been created and saved to 'password_list.txt'.")

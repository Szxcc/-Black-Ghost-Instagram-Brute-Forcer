import random
import re

# ------------------ Collect User Inputs ------------------
print("\n📝 Enter target information to generate a custom Instagram password list:")
first_name = input("First Name: ").strip()
last_name = input("Last Name: ").strip()
username = input("Instagram Username: ").strip()
birthday = input("Birthday (YYYY-MM-DD): ").strip()

# Parse birthday
try:
    year, month, day = birthday.split('-')
except:
    print("\n❌ Invalid birthday format. Please use YYYY-MM-DD.")
    exit(1)

common_numbers = ['123', '1234', '12345', '321', '1122', '2020', '111', '007', '786']
special_chars = ['', '!', '.', '_', '@']

# ------------------ Generate Base Words ------------------
base_words = [
    first_name,
    last_name,
    username,
    first_name + last_name,
    last_name + first_name,
    first_name + year,
    first_name + month,
    first_name + day,
    last_name + year,
    last_name + month,
    last_name + day,
    username + year,
    username + month,
    username + day
]

# Add base words with special chars
for word in base_words[:]:
    for ch in special_chars:
        base_words.append(word + ch)

# ------------------ Create Password Variations ------------------
passwords = set()

for word in base_words:
    for num in common_numbers:
        passwords.add(word + num)
        passwords.add(num + word)
    passwords.add(word)
    passwords.add(word.lower())
    passwords.add(word.upper())
    passwords.add(word.capitalize())

# Leet transformations
leet_map = {
    'a': ['4', '@'],
    'i': ['1', '!'],
    'e': ['3'],
    'o': ['0'],
    's': ['5', '$']
}

def leet_transform(word):
    variations = set()
    for _ in range(2):
        temp = word
        for letter, subs in leet_map.items():
            if random.random() < 0.5:
                temp = re.sub(letter, random.choice(subs), temp, flags=re.IGNORECASE)
        variations.add(temp)
    return variations

for word in base_words:
    passwords.update(leet_transform(word))

# ------------------ Save to File ------------------
passwords = list(passwords)
random.shuffle(passwords)

output_file = "passwords.txt"
with open(output_file, 'w') as f:
    for pwd in passwords:
        f.write(pwd + '\n')

print(f"\n✅ Password list generated! Total: {len(passwords)} passwords.")
print(f"💾 Saved to: {output_file}")
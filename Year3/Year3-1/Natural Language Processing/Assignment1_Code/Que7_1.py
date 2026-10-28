import re

# phone = input("Please enter a phone number: ")
phone = "1234-5678"

# pattern = r"^\d{4}-\d{4}$"
pattern = r"\b\d{4}-\d{4}\b"

if re.match(pattern, phone):
    print("Valid phone number")
else:
    print("Invalid phone number")
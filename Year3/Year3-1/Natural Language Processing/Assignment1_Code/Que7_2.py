import re

price = "972.50"

pattern = r"^\d+\.\d{2}$"

if re.match(pattern, price):
    print("Valid price")
else:
    print("Invalid price")
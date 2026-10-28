import re

word = "BOOK"

pattern = r"\b[A-Z]+\b"

if re.match(pattern, word):
    print("Valid uppercase word")
else:
    print("Invalid word")
import re

word = "JUMPing and Swimming"

pattern = r"\b[A-Za-z]+ing\b"

if re.match(pattern, word):
    print("Valid word")
else:
    print("Invalid word")
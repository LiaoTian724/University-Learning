import re

# text = input("Please enter a sentence: ")
text = "We use NLP technologies to automatically detect grammatical and spelling errors in textbooks for improving its quality"

# 提取真正的单词，并统一转成小写
words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

N = len(words)

unique_words = set(words)
V = len(unique_words)

lexical_diversity = V / N if N > 0 else 0

print("Words:", words)
print("Unique words:", sorted(unique_words))
print("N =", N)
print("|V| =", V)
print("Lexical Diversity =", round(lexical_diversity, 4))
import nltk
from sklearn.model_selection import train_test_split

sentences = list(nltk.corpus.treebank.tagged_sents())

print("Sentence length:", len(sentences))
print("First Sentence:", sentences[0])

X = []
y = []

for sent in sentences:
    words = []
    tags = []

    for word, tag in sent:
        words.append(word)
        tags.append(tag)

    X.append(words)
    y.append(tags)


# print("Words:", X)
# print("Tags:", y)

# Split the training set and testing set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training sentences:", len(X_train))
print("Testing sentences:", len(X_test))
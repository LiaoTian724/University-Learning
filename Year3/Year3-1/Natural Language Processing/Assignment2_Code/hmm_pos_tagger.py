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
print("================================")

# Training
emission_counts = {}        # eg:  {("DT", "The"): 1, ("NN", "cat"): 1, ("VBZ", "eats"): 1}
tag_counts = {}             # eg:  {"DT": 1, "NN": 1, "VBZ": 1}
transition_counts = {}      # eg:  {("<START>", "DT"): 1, ("DT", "NN"): 1, ("NN", "VBZ"): 1, ("VBZ", "<END>"): 1}

for words, tags in zip(X_train, y_train):
    previous_tag = '<START>'

    for i in range(len(words)):
        word = words[i]
        tag = tags[i]

        tag_counts[i] = tag_counts.get(tag, 0) + 1      # if tag_count[i]对应的词性数量为 0,返回 0+1; 如果存在,返回真正的数+1

        pair = (previous_tag, tag)
        transition_counts[pair] = transition_counts.get(pair, 0) + 1
        # print(pair)                      # ('<START>', 'NNS')
        # print(transition_counts)         # {('<START>', 'NNP'): 2, ('<START>', ','): 1, ('<START>', 'CD'): 1, ('<START>', 'NNS'): 1}
        # print("----")

        pair = (tag, word)
        emission_counts[pair] = emission_counts.get(pair, 0) + 1

        previous_tag = tag

    pair = (previous_tag, "<END>")
    transition_counts[pair] = transition_counts.get(pair, 0) + 1


print("Number of tags:", len(tag_counts))
print("DT to NN:", transition_counts.get(("DT","NN"),0))
print("NN emits 'company:", emission_counts.get(("NN","company"),0))
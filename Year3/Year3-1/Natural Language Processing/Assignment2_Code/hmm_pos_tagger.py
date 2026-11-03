import nltk
from sklearn.model_selection import train_test_split
from math import log

sentences = list(nltk.corpus.treebank.tagged_sents())

print("Total sentences:", len(sentences))
print("First Sentence:", sentences[0])

X = []
y = []

for sent in sentences:
    words = []
    tags = []

    for word, tag in sent:
        if tag == "-NONE-":
            continue
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

# Words: The  cat  eats
# Tags:  DT   NN   VBZ
for words, tags in zip(X_train, y_train):
    previous_tag = '<START>'

    for i in range(len(words)):
        word = words[i]
        tag = tags[i]

        # if tag_count[i]对应的词性数量为 0,返回 0+1; 如果存在,返回真正的数+1
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1
        # tag_counts[i] = tag_counts.get(tag, 0) + 1      

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


# print("Number of tags:", len(tag_counts))
# print("DT count:", tag_counts.get("DT", 0))
# print("DT to NN:", transition_counts.get(("DT","NN"),0))
# print("NN emits company:", emission_counts.get(("NN","company"),0))
# print("NN emits cat:", emission_counts.get(("NN", "cat"), 0))



# Calculate Initial Probability
initial_probs_mle = {}

for tag in tag_counts:          # eg:  {"DT": 1, "NN": 1, "VBZ": 1}
    count = transition_counts.get(("<START>", tag), 0)
    initial_probs_mle[tag] = count / len(X_train)
    # print(f"Initial Probability P({tag}|<START>) = {initial_probs_mle[tag]}")



# Calculate Transition Probability
transition_probs_mle = {}

for pair in transition_counts:
    previous_tag = pair[0]
    current_tag = pair[1]

    if previous_tag != "<START>":
        count = transition_counts[pair]
        # print(count)
        # transition_probs_mle[pair] = count / tag_counts[previous_tag]


# Calculate Emission Probability
emission_probs_mle = {}

# pair 只拿到了 ("DT", "The") 这种形式, 也就是词性和单词的组合; 因为遍历字典默认字典的 key, 所以 pair 就是 emission_counts 的 key
for pair in emission_counts:        # eg:  {("DT", "The"): 1, ("NN", "cat"): 1, ("VBZ", "eats"): 1}
    tag = pair[0]
    word = pair[1]

    count = emission_counts[pair]
    emission_probs_mle[pair] = count / tag_counts[tag]




# # Show some probabilities
# print("\nInitial Probability:")
# print(initial_probs_mle)

# print("\nTransition Probability:")
# print(list(transition_probs_mle.items())[:10])

# print("\nEmission Probability:")
# print(list(emission_probs_mle.items())[:10])





# Laplace Smoothing

# Get all tags
# eg:  tag_counts:  {"DT": 1, "NN": 1, "VBZ": 1}
tag_list = list(tag_counts.keys())      # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']

# Get all unique words from training data
vocabulary = set()
for words in X_train:
    for word in words:
        vocabulary.add(word)

vocabulary.add("<UNK>")  # Add <UNK> token for unknown words

# print('Number of unique tags:', len(tag_list))
# print("Vocabulary size:", len(vocabulary))



# Calculate Initial Probability with Laplace Smoothing
initial_probs_smooth = {}

for tag in tag_list:
    count = transition_counts.get(("<START>", tag), 0)       # eg:  {("<START>", "DT"): 1, ("DT", "NN"): 1, ("NN", "VBZ"): 1, ("VBZ", "<END>"): 1}
    initial_probs_smooth[tag] = (count + 1) / (len(X_train) + len(tag_list))


# Calculate Transition Probability with Laplace Smoothing
transition_probs_smooth = {}
next_tags = tag_list + ["<END>"]  # Add <END> to the list of next tags

for previous_tag in tag_list:     # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
    for current_tag in next_tags:  # next_tags: ['NNP', ',', 'CD', 'NNS', 'JJ', '<END>']
        pair = (previous_tag, current_tag)      # eg: ('NNP', 'NNP'), ('NNP', ','), ('NNP', 'CD'), ('NNP', 'NNS'), ('NNP', 'JJ'), ('NNP', '<END>')
        count = transition_counts.get(pair, 0)   # eg:  {("<START>", "DT"): 1, ("DT", "NN"): 1, ("NN", "VBZ"): 1, ("VBZ", "<END>"): 1}
        transition_probs_smooth[pair] = (count + 1) / (tag_counts[previous_tag] + len(next_tags))  # tag_counts  eg:  {"DT": 1, "NN": 1, "VBZ": 1}


# Calculate Emission Probability with Laplace Smoothing
emission_probs_smooth = {}

for tag in tag_list:    # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
    for word in vocabulary:  # vocabulary: {'company', 'The', 'cat', 'eats', '<UNK>'}
        pair = (tag, word)    # eg: ('NNP', 'company'), ('NNP', 'The'), ('NNP', 'cat'), ('NNP', 'eats'), ('NNP', '<UNK>')
        count = emission_counts.get(pair, 0)  # eg:  {("DT", "The"): 1, ("NN", "cat"): 1, ("VBZ", "eats"): 1}
        emission_probs_smooth[pair] = (count + 1) / (tag_counts[tag] + len(vocabulary))  # tag_counts  eg:  {"DT": 1, "NN": 1, "VBZ": 1}

    

# # Check smoothed probabilities

# print("\nSmoothed Initial Probability:")
# print("P(DT):", initial_probs_smooth.get("DT"))

# print("\nSmoothed Transition Probability:")
# print("P(NN|DT):", transition_probs_smooth.get(("DT", "NN")))

# print("\nSmoothed Emission Probability:")
# print("P(cat|NN):", emission_probs_smooth.get(("NN", "cat")))

# print("\nUnknown Word:")
# print("P(<UNK>|NN):", emission_probs_smooth.get(("NN", "<UNK>")))

# print("\nSum of Initial Probabilities:")
# print(sum(initial_probs_smooth.values()))








# Viterbi Algorithm
def viterbi(words):
    # Store the maximum probability at each position
    viterbi_table = []

    # Store the previous tag of the best path
    backpointer = []

    # Initialize the first column of the Viterbi table
    first_word = words[0]
    if first_word not in vocabulary:
        first_word = "<UNK>"

    first_scores = {}
    for tag in tag_list:        # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
        score = log(initial_probs_smooth[tag]) + log(emission_probs_smooth[(tag, first_word)])
        first_scores[tag] = score

    # First Scores: {'NNP': -11.450855018322326, ',': -17.64934246044035, 'CD': -17.64934246044035}
    viterbi_table.append(first_scores)      #[{'NNP': -11.450855018322326, ',': -17.64934246044035, 'CD': -14.07590682659161}]

    # Process the remaining words
    for i in range(1, len(words)):
        word = words[i]
        if word not in vocabulary:
            word = "<UNK>"

        current_scores = {}
        current_back = {}

        for current_tag in tag_list:        # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
            best_score = float("-inf")
            best_prev_tag = None

            for previous_tag in tag_list:   # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
                score = viterbi_table[i-1][previous_tag] + log(transition_probs_smooth[(previous_tag, current_tag)]) + log(emission_probs_smooth[(current_tag, word)])

                if score > best_score:
                    best_score = score
                    best_prev_tag = previous_tag

            current_scores[current_tag] = best_score
            current_back[current_tag] = best_prev_tag

        viterbi_table.append(current_scores)
        backpointer.append(current_back)



    # Find the best final tag
    best_score = float("-inf")
    best_tag = None

    for tag in tag_list:        # tag_list: ['NNP', ',', 'CD', 'NNS', 'JJ']
        score = (viterbi_table[-1][tag] + log(transition_probs_smooth[(tag, "<END>")]))

        if score > best_score:
            best_score = score
            best_tag = tag



    # Backtracking
    best_tags = [best_tag]

    for i in range(len(words) - 1, 0, -1):
        best_tag = backpointer[i-1][best_tag]
        best_tags.append(best_tag)

    best_tags.reverse()
    return best_tags




# # Test Viterbi
# test_words = X_test[0]

# predicted_tags = viterbi(test_words)

# print("\nTest Sentence:")
# print(test_words)

# print("\nActual Tags:")
# print(y_test[0])

# print("\nPredicted Tags:")
# print(predicted_tags)







# Evaluation
correct = 0
total = 0

for words, actual_tags in zip(X_test, y_test):
    predicted_tags = viterbi(words)

    for predicted, actual in zip(predicted_tags, actual_tags):
        if predicted == actual:
            correct += 1
        total += 1

accuracy = correct / total * 100

print("\n========== Evaluation ==========")
print("Correct predictions:", correct)
print("Total words:", total)
print("Accuracy:", round(accuracy, 2), "%")
print("================================\n")



# Show incorrect predictions

error_count = 0

for words, actual_tags in zip(X_test, y_test):

    predicted_tags = viterbi(words)

    for word, actual, predicted in zip(words, actual_tags, predicted_tags):

        if actual != predicted:
            print("Word:", word)
            print("Actual:", actual)
            print("Predicted:", predicted)
            print("----------------")

            error_count += 1

        if error_count == 10:
            break

    if error_count == 10:
        break
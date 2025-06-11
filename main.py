import random


reader = open("data/jekyll.txt")
successor_map = {}
window = []

for line in reader:
    for word in line.split():
        # clean_word = word.strip(".;,-“’”:?—‘!()_").lower()
        window.append(word)

        if len(window) == 3:
            key = window[0], window[1]
            value = window[2]
            if key in successor_map:
                successor_map[key].append(value)
            else:
                successor_map[key] = [value]
            window.pop(0)


# random.seed(3)
# word1 & word2 need to form a bigram that is present in the source text
word1 = "The"
word2 = "lawyer"

for i in range(15):
    print(word1, end=" ")
    successors = successor_map[(word1, word2)]
    word3 = random.choice(successors)
    word1, word2 = word2, word3

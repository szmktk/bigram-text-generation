import random


reader = open("data/jekyll.txt")
successor_map = {}
window = []

for line in reader:
    for word in line.split():
        clean_word = word.strip(".;,-“’”:?—‘!()_").lower()
        window.append(clean_word)

        if len(window) == 2:
            key = window[0]
            value = window[1]
            if key in successor_map:
                successor_map[key].append(value)
            else:
                successor_map[key] = [value]
            window.pop(0)


word = "the"
print(word, end=" ")


for i in range(15):
    successors = successor_map[word]
    word = random.choice(successors)
    print(word, end=" ")

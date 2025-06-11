import argparse
import random

# set the seed of PRNG to get predictive results
# random.seed(3)


def main() -> None:
    reader = open(args.input_file_path)
    successor_map = {}
    window = []

    for line in reader:
        for word in line.split():
            clean_word = word.strip(".;,-“’”:?—‘!()_").lower()
            window.append(clean_word)

            if len(window) == 3:
                key = window[0], window[1]
                value = window[2]
                if key in successor_map:
                    successor_map[key].append(value)
                else:
                    successor_map[key] = [value]
                window.pop(0)

    initial_bigram = tuple(args.initial_bigram.split(","))
    word1, word2 = initial_bigram

    for _ in range(15):
        print(word1, end=" ")
        successors = successor_map[(word1, word2)]
        word3 = random.choice(successors)
        word1, word2 = word2, word3

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate text from a text file using bigrams."
    )
    parser.add_argument("input_file_path", help="Path to the input text file.")
    parser.add_argument(
        "--initial-bigram",
        "-i",
        help="Comma-separated words to start generation. They need to form a bigram that is present in the source text. Default is 'the,lawyer'.",
        default="the,lawyer",
    )
    args = parser.parse_args()
    main()

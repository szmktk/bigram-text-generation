import argparse
import random
from collections import Counter

# set the seed of PRNG to get predictable results
# random.seed(3)


def main() -> None:
    reader = open(args.input_file_path)
    bigram_counts = Counter()
    successor_map = {}
    window = []

    for line in reader:
        for word in line.split():
            clean_word = (
                word.strip(".;,-“’”:?—‘!()_").lower() if args.clean_words else word
            )
            window.append(clean_word)

            if len(window) == 3:
                key = window[0], window[1]
                value = window[2]
                if key in successor_map:
                    successor_map[key].append(value)
                else:
                    successor_map[key] = [value]
                bigram_counts[key] += 1
                window.pop(0)

    if args.top_bigrams > 0:
        print_most_common_bigrams(bigram_counts, args.top_bigrams)

    initial_bigram = (
        tuple(args.initial_bigram.split(","))
        if args.initial_bigram
        else choose_random_bigram(bigram_counts, args.print_bigram)
    )
    word1, word2 = initial_bigram

    for _ in range(15):
        print(word1, end=" ")
        successors = successor_map[(word1, word2)]
        word3 = random.choice(successors)
        word1, word2 = word2, word3

    print()


def print_most_common_bigrams(bigram_counts: Counter, n_common_bigrams: int) -> None:
    print(f"Top {n_common_bigrams} most common bigrams:")
    for bigram, count in bigram_counts.most_common(n_common_bigrams):
        print(f"{bigram}: {count}")
    print()


def choose_random_bigram(bigram_counts: Counter, print_bigram: bool) -> tuple[str, str]:
    top_bigrams = bigram_counts.most_common(50)
    if not top_bigrams:
        raise ValueError("Not enough bigrams available to choose from.")

    chosen_bigram = random.choice([bigram for bigram, _ in top_bigrams])
    if print_bigram:
        print(f"Randomly chosen bigram: {chosen_bigram}")
    return chosen_bigram


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate text from a text file using bigrams."
    )
    parser.add_argument("input_file_path", help="Path to the input text file.")
    parser.add_argument(
        "--initial-bigram",
        "-i",
        help="Comma-separated words to start generation. They need to form a bigram that is present in the source text.",
    )
    parser.add_argument(
        "--no-clean",
        "-n",
        action="store_false",
        dest="clean_words",
        help="Disable word cleaning (stripping punctuation and converting to lowercase).",
    )
    parser.add_argument(
        "--top-bigrams",
        "-t",
        type=int,
        default=0,
        help="Print top N most common bigrams found in the source text.",
    )
    parser.add_argument(
        "--print-bigram",
        "-p",
        action="store_true",
        help="Print the randomly chosen bigram among the top N bigrams.",
    )
    args = parser.parse_args()
    main()

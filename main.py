import argparse
import glob
import os
import random
from collections import Counter
from io import TextIOWrapper

# set the seed of PRNG to get predictable results
# random.seed(3)


def main() -> None:
    # bigram_counts = Counter()
    # successor_map = {}

    successor_map, bigram_counts = process_files(args.input_dir, args.clean_words)

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
        successors = successor_map.get((word1, word2), None)
        if not successors:
            break
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


def process_files(input_dir: str, clean_words: bool) -> tuple[dict, Counter]:
    successor_map = {}
    bigram_counts = Counter()
    for file_path in glob.glob(os.path.join(input_dir, "*.txt")):
        with open(file_path, "r") as reader:
            process_reader(reader, successor_map, bigram_counts, clean_words)
    return successor_map, bigram_counts


def process_reader(
    reader: TextIOWrapper,
    successor_map: dict,
    bigram_counts: Counter,
    clean_words: bool,
) -> None:
    # TODO can we move the window deeper?
    window = []
    for line in reader:
        for word in line.split():
            clean_word = word.strip(".;,-“’”:?—‘!()_").lower() if clean_words else word
            update_window_and_maps(window, clean_word, successor_map, bigram_counts)


def update_window_and_maps(
    window: list, clean_word: str, successor_map: dict, bigram_counts: Counter
):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate text from .txt files using bigrams."
    )
    parser.add_argument(
        "--input-dir",
        "-d",
        help="Path to the directory with text files. Default is 'data'.",
        default="data",
    )
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

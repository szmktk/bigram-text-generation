import argparse
import glob
import os
import random
import sys
from collections import Counter
from io import TextIOWrapper

from memory_profiler import profile

# set the seed of PRNG to get predictable results
# random.seed(3)


def main() -> None:
    global process_reader
    process_reader = (
        profile(_process_reader) if args.profile_memory else _process_reader
    )
    process_files = profile(_process_files) if args.profile_memory else _process_files

    bigram_counts = Counter()
    successor_map = {}

    process_files(successor_map, bigram_counts)  # type: ignore

    if args.top_bigrams > 0:
        print_most_common_bigrams(bigram_counts, args.top_bigrams)

    initial_bigram = (
        tuple(args.initial_bigram.split(","))
        if args.initial_bigram
        else choose_random_bigram(bigram_counts, args.print_bigram)
    )
    word1, word2 = initial_bigram

    for _ in range(args.num_words):
        successors = successor_map.get((word1, word2), None)
        if not successors:
            sys.exit(f"Bigram {initial_bigram} not found in source text corpus")
        print(word1, end=" ")
        word3 = random.choice(successors)
        word1, word2 = word2, word3

    print()


def print_most_common_bigrams(bigram_counts: Counter, n_common_bigrams: int) -> None:
    print(f"Top {n_common_bigrams} most common bigrams:")
    for bigram, count in bigram_counts.most_common(n_common_bigrams):
        print(f"{bigram}: {count}")
    print()


def choose_random_bigram(bigram_counts: Counter, print_bigram: bool) -> tuple[str, str]:
    top_bigrams = bigram_counts.most_common(args.top_bigrams_to_choose)
    if not top_bigrams:
        sys.exit("Not enough bigrams available to choose from.")

    chosen_bigram = random.choice([bigram for bigram, _ in top_bigrams])
    if print_bigram:
        print(f"Randomly chosen bigram: {chosen_bigram}")
    return chosen_bigram


def _process_files(successor_map: dict, bigram_counts: Counter) -> None:
    if not os.path.exists(args.input_dir):
        sys.exit(f"Error: The input directory '{args.input_dir}' does not exist.")

    for file_path in glob.glob(os.path.join(args.input_dir, "*.txt")):
        with open(file_path, "r") as reader:
            process_reader(reader, successor_map, bigram_counts)  # type: ignore


def _process_reader(
    reader: TextIOWrapper, successor_map: dict, bigram_counts: Counter
) -> None:
    window = []
    for line in reader:
        for word in line.split():
            clean_word = (
                word.strip(".;,-“’”:?—‘!()_").lower() if args.clean_words else word
            )
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
    parser.add_argument(
        "--num-words",
        "-w",
        type=int,
        default=15,
        help="Number of words to generate. Default is 15.",
    )
    parser.add_argument(
        "--top-bigrams-to-choose",
        "-tb",
        type=int,
        default=50,
        help="Number of top bigrams to consider for choosing starting bigram. Default is 50.",
    )
    parser.add_argument(
        "--profile-memory",
        "-x",
        action="store_true",
        help="Enable memory profiling (when memory-profiler is installed).",
    )
    args = parser.parse_args()
    main()

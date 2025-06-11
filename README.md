# Text Generation in Python Using Bigrams

This script reads text files, analyzes word pairs ([bigrams](https://en.wikipedia.org/wiki/Bigram)), and generates text based on these pairs. It leverages the frequency of bigrams to predict and construct new sequences of words.


## Purpose

The main purpose of this script is to take one or more text files, compute the frequency of bigrams, and then use these bigrams to generate new, moderately coherent text sequences. This is useful for understanding text construction techniques, random text generation, and experimenting with prediction algorithms.


## Prerequisites

Ensure you have Python installed on your system. This script is confirmed to run with Python 3.9.

The script processes all `.txt` files within a specified directory ([`data`](./data/) by default).


## Usage

Run the script from the command line with the following options:

```bash
❯ python3 main.py -h
usage: main.py [-h] [--input-dir INPUT_DIR] [--initial-bigram INITIAL_BIGRAM] [--no-clean] [--top-bigrams TOP_BIGRAMS] [--print-bigram] [--num-words NUM_WORDS] [--top-bigrams-to-choose TOP_BIGRAMS_TO_CHOOSE]

Generate text from .txt files using bigrams.

options:
  -h, --help            show this help message and exit
  --input-dir, -d INPUT_DIR
                        Path to the directory with text files. Default is 'data'.
  --initial-bigram, -i INITIAL_BIGRAM
                        Comma-separated words to start generation. They need to form a bigram that is present in the source text.
  --no-clean, -n        Disable word cleaning (stripping punctuation and converting to lowercase).
  --top-bigrams, -t TOP_BIGRAMS
                        Print top N most common bigrams found in the source text.
  --print-bigram, -p    Print the randomly chosen bigram among the top N bigrams.
  --num-words, -w NUM_WORDS
                        Number of words to generate. Default is 15.
  --top-bigrams-to-choose, -tb TOP_BIGRAMS_TO_CHOOSE
                        Number of top bigrams to consider for choosing starting bigram. Default is 50.
```


## Examples

Analyzes the text files in the default data directory, prints the top 10 most common bigrams, and disables word cleaning (i.e., keeps punctuation and original casing):
```bash
python3 main.py -t 10 -n
```

Prints the top 20 bigrams from the input files and randomly selects and displays one of them as the initial bigram for text generation:
```bash
python3 main.py -t 20 -p
```

Starts text generation using the bigram "The lawyer" as the seed. Word cleaning is disabled, so exact casing and punctuation matter when matching the initial bigram:
```bash
python3 main.py -i The,lawyer -n
```

Generates 25 words of text, selecting the initial bigram randomly from the top 10 most frequent bigrams, and prints the top 10 bigrams from the source text:
```bash
python3 main.py -w 25 -tb 10 -t 10
```

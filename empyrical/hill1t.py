import json
import os
import re
from collections import Counter
from math import ceil

import matplotlib.pyplot as plt
import numpy as np
import spacy
from tqdm import tqdm


def get_config():
    """
    Fetch the config data for the script, look in `config.json` under `hill1t`

    Returns:
        dict: The config as a dictionary, see `config.json`
    """
    with open('config.json', 'r') as f:
        return json.loads(f.read())["hill1t"]


def find_text_files(directory):
    """
    Find all the text files in the provided `directory`.

    `directory` will be searched recursively for all `.txt` files.

    Parameters:
        directory (str): The directory to search

    Returns:
        list[str]: The paths of all `.txt` files identified
    """
    files = []
    for subdir, dirs, fs in tqdm(os.walk(os.path.abspath(directory)), desc="Scanning for Text"):
        for f in fs:
            if f.endswith('.txt'):
                files.append(os.path.join(subdir, f))
    return files


def compile_texts(files):
    """
    Given a list of files, compile the raw text of all files into one list.

    The text will undergo a cleaning process which may lightly modify it for easier parsing. Currently the cleaning process is limited to removing unnecessary whitespace.

    Parameters:
        files (list[str]): A list of file paths to compile

    Returns:
        list[str]: The cleaned text from each file, listed per-file
    """
    texts = []
    for path in tqdm(files, desc="Reading Raw Text"):
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())
    # Tone down whitespace if text is heavily indented
    return [re.sub(r"\s+", " ", text.strip()) for text in texts]


def get_sentences(lang, texts):
    """
    Use Spacy to identify sentences in texts.

    Parameters:
        lang (spacy.lang): The Spacy language model to use for parsing
        texts (list[str]): The list of texts to parse

    Returns:
        list[spacy.Span]: A list of all sentences encountered
    """
    sentences = []
    for text in tqdm(texts, desc="Parsing Text"):
        sentences += lang(text).sents
    return sentences


def process(sentences):
    """
    Use Spacy's parsed document information to process a list of sentences.

    Parameters:
        sentences (list[spacy.Span]): A list of sentences to process

    Returns:
        list[list[str]]: Each sentence as a list of lemmatized words
    """
    processed = []
    for sentence in tqdm(sentences, desc="Extracting Lemmas"):
        processed.append(
            [
                token.lemma_
                for token in sentence
                # Ignore punctuation, spaces, and proper nouns
                if token.pos_ not in {"PUNCT", "SPACE", "PROPN"}
            ]
        )
    return [s for s in processed if len(s) > 0]


def language_preprocessing(spacy_model, texts):
    """
    Use Spacy to fetch information about a list of texts.

    Parameters:
        spacy_model (spacy.lang): The Spacy language model to use for processing
        texts (list[str]): The list of raw texts as strings to process

    Returns:
        list[list[obj]]: Each sentence as a processed object, see `process()`
    """
    sentences = get_sentences(spacy_model, texts)
    return process(sentences)


def get_freq_list(processed):
    """
    Convert a list of processed sentences into a frequency list.

    Parameters:
        processed (list[list[obj]]): The processed sentences
    
    Returns:
        list[tuple[str, int]]: A sorted list of word-frequency pairs, descending by frequency
    """
    word_freqs = Counter(w for s in processed for w in s)
    return sorted(word_freqs.items(), key=lambda x: x[1], reverse=True)


def count_1ts(word_freqs, processed):
    """
    Count the 1T sentences encountered at each stage of learning a frequency list.

    Parameters:
        word_freqs (list[tuple[str, int]]): A frequency list of word-frequency pairs
        processed (list[list[obj]]): A list of processed sentences
    
    Returns:
        dict[int, int]: For each amount of words known in [0, len(freq_list)), the amount of 1T sentences
    """
    counts = Counter()
    for i in tqdm(range(len(freq_list)), desc="Computing Data"):
        counts[i] = 0
        known = set(map(lambda x: x[0], freq_list[:i]))
        for sentence in processed:
            if len(set(sentence) - known) == 1:
                counts[i] += 1
    return counts


def plot_1ts(count1ts, freq_list):
    """
    Given the information about 1T sentences, display it with matplotlib

    Parameters:
        count1ts (dict[int, int]): The data for the frequencies of 1Ts, see `count_1ts()`
        freq_list (list[tuple[str, int]]): A frequency list of word-frequency pairs
    """

    # Data for axes
    freq_total = sum(f[1] for f in freq_list)
    count_x = [c[0] for c in count1ts]
    count_y = [c[1] for c in count1ts]
    freq_y = [100 * sum(f[1] for f in freq_list[:i]) /
              freq_total for i in count_x]

    # Plot the 1T sentences against words known
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Words Known")
    ax1.set_ylabel("1T Frequency", color="blue")
    ax1.plot(count_x, count_y, color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ylim = ceil((max(count_y) + 10) / 100) * 100
    ax1.yaxis.set_ticks(np.linspace(0, ylim, 11))
    ax1.set_ylim(0, ylim)
    ax1.set_xlim(0, max(count_x))
    ax1.grid(True)

    # Plot the comprehensibility (% of words known)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Comprehensibility", color="red")
    ax2.plot(count_x, freq_y, color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.set_ylim(0, 100)
    ax2.set_xlim(0, max(count_x))
    ax2.yaxis.set_ticks(np.linspace(0, 100, 11))

    # Display
    plt.show()


if __name__ == "__main__":
    CONFIG = get_config()
    # Get raw text
    files = find_text_files(CONFIG["text_path"])
    texts = compile_texts(files)
    # Boring preprocessing
    processed = language_preprocessing(
        spacy.load(CONFIG["spacy_pipeline"]), texts)
    # Fun postprocessing
    freq_list = get_freq_list(processed)
    counts = count_1ts(freq_list, processed)
    plot_1ts(counts.items(), freq_list)

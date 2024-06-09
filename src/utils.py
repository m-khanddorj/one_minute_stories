import os
import json
import random

def read_random_line(folder_path):
    """
    Reads a random line from the specified text file.

    :param folder_path: Path to the text file.
    :return: A random line from the file.
    """
    with open(folder_path, "r") as file:
        lines = file.readlines()

    if not lines:
        return None  # Return None if the file is empty

    random_line = random.choice(lines)
    return random_line.strip()


def split_story_into_sentences(story):
    """Split a story into sentences."""
    import nltk

    sentences = nltk.sent_tokenize(story)
    return sentences


def select_random_file(folder_path):
    import os

    files = os.listdir(folder_path)
    choice = random.choice(files)

    return os.path.join(folder_path, choice)


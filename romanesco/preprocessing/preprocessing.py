import argparse
import os
import re

from nltk.tokenize import word_tokenize

PATH = os.path.abspath(os.path.dirname(__file__))


def parse_args() -> argparse.Namespace:
    """ Parse arguments given via command lines"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-trg", "--target",  required=True,
                        action="store", dest="trg", help="target text for preprocessing")
    args = parser.parse_args()

    return args


def tokenize(sentence: str) -> list:
    """ Tokenize a given text """
    # tokenize sentence with nltk tokenizer
    tokenized = word_tokenize(sentence)
    return tokenized


def read_file(file_name):
    """ Read file and return text """
    with open(os.path.join(PATH, file_name), 'r') as fp:
        text = fp.read()

    return text


def prepare_text(text: str):
    """ Prepare text for tokenization"""
    text = re.sub(r'-', ' ', text)
    text = re.sub(r'\d', '', text)
    text = re.sub(r'—', '', text)
    return text.lower()


def main(args):
    file_name = args.trg
    text = read_file(file_name)
    text = prepare_text(text)
    tokenized_text = tokenize(text)
    all_sentence = []
    for i, word in enumerate(tokenized_text):
        if word.isdigit():
            continue

        try:
            if word in ('.', '!', '?') and tokenized_text[i+1] != ')':
                word += '\n'
        except IndexError:
            pass

        all_sentence.append(word)

    with open(os.path.join(PATH, 'processed_' + file_name), 'w') as fp:
        fp.write(' '.join(all_sentence))


if __name__ == '__main__':
    args = parse_args()
    main(args)

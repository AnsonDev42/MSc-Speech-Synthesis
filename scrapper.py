# scrap to sentences from the given text
import os
import random

import nltk, re, pprint
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, RegexpTokenizer


def first_time_setup():
    nltk.download('punkt')
    nltk.download('words')


# first_time_setup()

def text_file_loader():
    path = 'books'
    tokenizer = nltk.data.load("tokenizers/punkt/PY3/english.pickle")
    files = os.listdir(path)
    all_contents = []
    for file in files:
        # get the full path to the file
        file_path = os.path.join(path, file)

        # open the file and read its contents
        with open(file_path, 'r') as f:
            raw = f.read()
            # remove \n
            for char in ["\n", "\r", "\d", "\t"]:
                raw = raw.replace(char, " ")
            # print(type(raw)) # str
            # sentences = tokenizer.tokenize(raw)
            # tokenize to sentences
            sentences = sent_tokenize(raw)
            all_contents += sentences
    return all_contents


# print(text_file_loader()[1])

def content_to_sentence():
    # nltk.download('punkt')
    words = set(nltk.corpus.words.words())  # dictionary of words
    all_contents = text_file_loader()
    filtered_contents = []
    # strip the beginning and the end
    for sentence in all_contents[50:-353]:
        # remove extra spaces e.g. ('hello    world'=> 'hello world')
        sentence = re.sub(r'\s+', ' ', sentence)
        if not (3 <= len(sentence.split()) <= 12):
            continue
        # check if the sentence contains a number
        # remove punctuation
        # sentence = re.sub(r'[^\w\s]', '', sentence)
        # remove double quotes
        sentence = re.sub(r'[”\“]', '', sentence)
        # remove numbers
        sentence = re.sub(r'\d+', '', sentence)
        # substitute ’ with '
        sentence = re.sub(r'’', "'", sentence)
        # remove characters that are non ascii
        sentence = re.sub(r'[^\x00-\x7F]+', '', sentence)
        # remove  -- since - is a valid english word
        sentence = re.sub(r'--', ' ', sentence)
        #  substitute words that is capitalized to "Tom"  using re, expect the first word
        sentence = re.sub(r'(?<=\s)[A-Z][a-z]+', 'Andy', sentence)
        filtered_contents.append(sentence)

    print(filtered_contents)
    return filtered_contents


def shuffle_create_test_train(sentences=[]):
    if sentences == []:
        sentences = content_to_sentence()
    # shuffle the sentences
    # random.shuffle(sentences)
    # split the sentences into train and test
    train = sentences[:int(len(sentences) * 0.6)]
    test = sentences[int(len(sentences) * 0.6):]
    # save train to file
    counter = 1

    # with open('train_unprocessed_sentence.txt', 'w') as f:
    #     for sentence in train:
    #         f.write(f'( c_books_train_{counter:04} "{sentence}" )\n')
    #         counter += 1
    #
    # # save test to file
    # with open('test_unprocessed_sentence.txt', 'w') as f:
    #     for sentence in test:
    #         f.write(f'( c_books_test_{counter:04} "{sentence}" )\n')
    #         counter += 1
    with open('utts.data', 'w') as f:
        for sentence in train:
            f.write(f'( c_books_test_{counter:04} "{sentence}" )\n')
            counter += 1
        for sentence in test:
            f.write(f'( c_books_test_{counter:04} "{sentence}" )\n')
            counter += 1

    return train, test


def get_train_data():
    with open('train_unprocessed_sentence.txt', 'r') as f:
        train = f.readlines()
    assert type(train) == list
    # print(train[0])
    return train


def greedy_picker(sentences=[]):
    if not sentences:
        sentences = get_train_data()
    assert len(sentences) > 0
    # pick the first sentence


# get_train_data()
shuffle_create_test_train()
# content_to_sentence()

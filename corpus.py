from logzero import logger

import pickle
import nltk
import os


class Corpus:

    def __init__(self, word_length: int = 0):
        self.word_length = word_length
        self.words = None
        self.__load_words(word_length)
        self.size = 0

    def __load_words(self, word_length: int = 5):
        if word_length <= 0:
            raise Exception('Must choose a word length greater than 0.')

        # This program works for all length words but we have a special list for 5 letter words
        if word_length != 5:
            words = nltk.corpus.words.words()
            self.words = [word.lower() for word in words if len(word) == word_length]
        else:
            if os.path.exists('five_letter_solutions.pickle'):
                with open('five_letter_solutions.pickle', 'rb') as fp:
                    self.words = list(pickle.load(fp))
            else:
                words = nltk.corpus.words.words()
                self.words = [word.lower() for word in words if len(word) == word_length]

        self.size = len(self.words)

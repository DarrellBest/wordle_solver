from corpus import Corpus
from random import choice


class Wordle:

    def __init__(self, corpus: Corpus):
        self.corpus = corpus
        self.words = self.corpus.words
        self.word_length = self.corpus.word_length
        self.__solution = choice(self.words)

    def restart(self):
        self.__solution = choice(self.words)

    def guess(self, word: str = '') -> list:
        word = word.lower()
        if len(word) != self.word_length:
            raise Exception(f'Word must be of length {self.word_length}.')
        if word not in self.words:
            raise Exception(f'String given is not a word in the given language.')

        result = []
        for i in range(self.word_length):
            if word[i] == self.__solution[i]:
                result.append(2)
            elif word[i] in self.__solution:
                result.append(1)
            else:
                result.append(0)

        return result

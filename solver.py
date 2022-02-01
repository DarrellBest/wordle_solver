from logzero import logger
from wordle import Wordle
from tqdm.contrib.concurrent import process_map
from collections import Counter
from scipy import stats
from typing import List

import statistics
import psutil


class Solver:

    def __init__(self, game: Wordle, simulations_per_word: int):
        self.game = game
        self.words = game.corpus.words
        self.filtered_words = game.corpus.words
        self.cpu_count = None
        self.set_cpu_affinity()
        self.letter_frequencies_by_pos = None
        self.simulations_per_word = simulations_per_word

    def set_cpu_affinity(self):
        p = psutil.Process()
        self.cpu_count = psutil.cpu_count()
        all_cpus = list(range(self.cpu_count))
        p.cpu_affinity(all_cpus)

    def filter_words(self, word_guess: str, result: List[int]):
        if word_guess in self.filtered_words:
            self.filtered_words.remove(word_guess)

        for i, (val, char) in enumerate(zip(result, word_guess)):
            if val == 2:
                self.filtered_words = [word for word in self.filtered_words if char == word[i]]
            if val == 1:
                self.filtered_words = [word for word in self.filtered_words if char != word[i] and char in word]
            if val == 0:
                self.filtered_words = [word for word in self.filtered_words if char not in word]

    def calculate_frequencies(self):
        self.letter_frequencies_by_pos = [Counter() for _ in range(self.game.word_length)]
        for i, counter in enumerate(self.letter_frequencies_by_pos):
            for word in self.filtered_words:
                counter.update(word[i])

    def calculate_word_rank(self, word: str) -> int:
        value = 0
        for i, letter in enumerate(word):
            value += self.letter_frequencies_by_pos[i][letter]

        return value

    def sort_words(self):
        self.calculate_frequencies()
        self.filtered_words = sorted(self.filtered_words, key=self.calculate_word_rank, reverse=True)

    def simple_experiment(self):
        choices = self.words
        # Im only using %80 of your CPU cores...
        result = process_map(self.simple_solve,
                             choices,
                             max_workers=int(self.cpu_count // 1.2),
                             chunksize=1)

        result_dict = {key: val for key, val in result}
        result_dict = dict(sorted(result_dict.items(), key=lambda x: statistics.mean(x[1]) ))
        result_list = list(result_dict.items())

        results = stats.ttest_ind(a=result_list[0][1], b=result_list[-1][1], equal_var=False)
        logger.info(f'\nTop 10 results are: \n{list(result_dict.keys())[:10]}')
        logger.info(f'\nWorst 10 results are: \n{list(result_dict.keys())[-10:]}')
        logger.info(f'\nBest word: {result_list[0][0]} \n'
                    f'Average turns to solve: {statistics.mean(result_list[0][1])} \n'
                    f'StD Dev: {statistics.stdev(result_list[0][1])} \n'
                    f'Success Rate: {((len(result_list[0][1])) / self.simulations_per_word) * 100}'
                    f'++++ \n'
                    f'Worst word: {result_list[-1][0]} \n'
                    f'Average turns to solve: {statistics.mean(result_list[-1][1])} \n'
                    f'StD Dev: {statistics.stdev(result_list[-1][1])} \n'
                    f'Success Rate: {((len(result_list[-1][1])) / self.simulations_per_word) * 100}'
                    f'++++\n\n'
                    f'pValue {results.pvalue}\n')

        if results.pvalue < 0.05:
            logger.info(f'Pvalue less than 0.05 so we reject the null hypothesis. '
                        f'(there is a significant difference)')
        else:
            logger.info(f'Pvalue greater than 0.05 so we do not reject the null hypothesis. '
                        f'(There is not a significant difference)')

    def simple_solve(self, word: str = '', logging: bool = False):
        solved_counts = []
        failed_count = 0

        for i in range(self.simulations_per_word):
            self.game.restart()
            self.filtered_words = self.words.copy()
            self.sort_words()
            steps = 0
            solved = False

            while not solved:
                steps += 1

                if logging:
                    logger.info(f'There are {len(self.filtered_words)} words remaining.')

                word_guess = word if word and steps == 1 else self.filtered_words[0]

                if logging:
                    logger.info(f'Guessing word: {word_guess}')

                result = self.game.guess(word_guess)

                if sum(result) == self.game.corpus.word_length * 2:
                    if logging:
                        logger.info(f'The solution has been found in {steps} steps!')
                    solved = True
                    if steps <= 6:
                        solved_counts.append(steps)
                    else:
                        failed_count += 1
                else:
                    self.filter_words(word_guess, result)

        if logging:
            logger.info(f'Solved with an average of {statistics.mean(solved_counts)} turns with a standard deviation of'
                        f' {statistics.stdev(solved_counts)}.')
            logger.info(f'Failed to solve {failed_count} times. Success rate is '
                        f'%{((self.simulations_per_word - failed_count) / self.simulations_per_word) * 100}')

        return word, solved_counts

    def help_me_solve(self):
        print('This is for educational purposes only. Please do not cheat or it ruins the fun!\n')
        print('Step 1. Go to https://www.powerlanguage.co.uk/wordle/')
        print('Step 2. Guess a word on the website')
        print('Step 3. Enter the word into this program at the prompt')
        print('Step 4. Enter your result in the prompt. ')
        print('Step 5. Repeat steps 1 - 4 until solved.')
        print('\nEnter the result as a 5 digit number. For example, the solution is DRANK and you TREAD. '
              'The solution number would look like 02011.')
        print('0: Letter not in word, 1: Letter is in the wrong position, 2: letter is in the correct position')

        self.filtered_words = self.words.copy()
        solved = False
        steps = 0

        while not solved:
            self.sort_words()
            print(f'\nMost likely word(s): {self.filtered_words[:10]}')
            word_guess = input('\nGuessed word: ')
            result = input('Result? Example 12002: ')
            result = [int(char) for char in result]
            steps += 1

            if sum(result) == self.game.corpus.word_length * 2:
                print(f'The solution has been found in {steps} steps!')
                solved = True
                steps = 0
            else:
                self.filter_words(word_guess, result)
                print(f'There are {len(self.filtered_words)} words remaining.')

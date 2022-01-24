from solver import Solver
from corpus import Corpus
from wordle import Wordle


def main():
    corpus = Corpus(word_length=5)
    game = Wordle(corpus=corpus)
    solver = Solver(game=game, simulations_per_word=100)
    solver.simple_experiment()
    # solver.simple_solve(logging=True, word='tread')
    # solver.simple_solve(logging=True)
    # solver.help_me_solve()


if __name__ == '__main__':
    main()

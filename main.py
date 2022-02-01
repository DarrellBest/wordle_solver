from solver import Solver
from corpus import Corpus
from wordle import Wordle


def main():
    corpus = Corpus(word_length=5)
    game = Wordle(corpus=corpus)
    solver = Solver(game=game, simulations_per_word=100)

    # Comment this line of code out if you want to run simple_solve or the help_me_solve function
    solver.simple_experiment()

    # You can run the simple solve function by itself to see how an individual word performs
    # solver.simple_solve(logging=True, word='queue')  # worst possible starting guess
    # solver.simple_solve(logging=True, word='slate')  # best possible starting guess

    # Please do not cheat, this function is just for fun.
    # solver.help_me_solve()


if __name__ == '__main__':
    main()

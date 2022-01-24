# wordle_solver
I got bored and wrote a world solver... Its pretty good though, just saying

TLDR--- Solves in 3.59 turns with a 99% success rate


This solver uses a combination of letter frequency calculations and word list pruning techniques.

I had two goals when writting this code:
1. Write a solver that works
2. Optimize using different techniques
3. Run an experiment to determine if there is a significant difference in the number of turns it takes to solve versus the starting word.

Here are the results of the experiment which can be replicated by running the code yourself.

Top 10 words to start with are:
    ['tread', 'raspy', 'lusty', 'grand', 'posit', 'shale', 'crust', 'lyric', 'tenor', 'horde']

Worst 10 words to start with are:
    ['kappa', 'pizza', 'affix', 'fuzzy', 'verve', 'amaze', 'motto', 'queue', 'expel', 'mimic']

    Best word to start with: tread
    Mean turns to solve: 3.595959595959596
    STD: 0.8912178313076166
    Success Rate: 99.0++++

    Worst word to start with: mimic
    Mean turns to solve: 4.515789473684211
    STD: 0.943771946564455
    Success Rate: 95.0++++
    pValue 4.966074332439964e-11

pValue less than 0.05 so we reject the null hypothesis. (there is a significant difference).
This just means it matters what word you start with.

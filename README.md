# wordle_solver
I got bored and wrote a wordle solver... Its pretty good though, just saying. Please go support Josh and have fun with Wordle on the official website https://www.powerlanguage.co.uk/wordle/

TLDR--- Solves in 3.59 turns with a 99% success rate


This solver uses a combination of letter frequency calculations and word list pruning techniques.

I had three goals when writting this code:
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

#######################################################################################################

The 'Help me solve' function is for educational purposes only. Please do not cheat or it ruins the fun!
If you want to use this function just uncomment the line in main.py before you run. 

- Step 1. Go to https://www.powerlanguage.co.uk/wordle/
- Step 2. Guess a word on the website
- Step 3. Enter the word into this program at the prompt
- Step 4. Enter your result in the prompt. 
- Step 5. Repeat steps 1 - 4 until solved.

Enter the result as a 5 digit number. For example, the solution is DRANK and you TREAD. The solution number would look like 02011.
0: Letter not in word, 1: Letter is in the wrong position, 2: letter is in the correct position


An example solve:

    Most likely word(s): ['slate', 'sauce', 'slice', 'shale', 'saute', 'share', 'sooty', 'shine', 'suite', 'crane']

    Guessed word: slate
    Result? Example 12002: 01000
    There are 87 words remaining.

    Most likely word(s): ['golly', 'dolly', 'folly', 'gully', 'dully', 'bully', 'holly', 'fully', 'jolly', 'dilly']

    Guessed word: golly
    Result? Example 12002: 01120
    There are 2 words remaining.

    Most likely word(s): ['droll', 'knoll']

    Guessed word: droll
    Result? Example 12002: 00222
    There are 1 words remaining.

    Most likely word(s): ['knoll']

    Guessed word: knoll
    Result? Example 12002: 22222
    The solution has been found in 4 steps!


import random
import pandas as pd
from simulator import guess_word, check, words

# seed_value = 200
# random.seed(seed_value)

answer = random.choices(words['words'], weights = words['freq'])[0]

print('answer: ', answer)
print('\n')

#-----------------------------------------------------------------------------

false_letters, true_letters, misplaced_letters, guess = [], {}, {}, None
tries = 0
while guess != answer:
    tries += 1
    guess, num_choices = guess_word(words, false_letters, true_letters, misplaced_letters)
    print(f'guessed "{guess}" out of {num_choices} choices')
    
    false_letters, true_letters, misplaced_letters = check(answer, guess, false_letters, true_letters, misplaced_letters)

    print('false_letters: ',false_letters)
    print('true_letters: ',true_letters)
    print('misplaced_letters: ',misplaced_letters)
    print('\n')

print('holy shit! it worked!')
print('tries: ',tries)   
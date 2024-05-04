import random
from sklearn.utils import shuffle
import pandas as pd

words = pd.read_csv('data/american-english_processed.csv')

def check(answer, guess, false_letters=None, true_letters=None, misplaced_letters=None):
    
    if false_letters is None:
        false_letters = []
    if true_letters is None:
        true_letters = {}
    if misplaced_letters is None:
        misplaced_letters = {}
    
    new_false_letters = []
    new_true_letters = {}
    new_misplaced_letters = {}
    
    for i, letter in enumerate(guess):
        if letter == answer[i]:
            new_true_letters[i] = letter
        elif letter in answer:
            new_misplaced_letters.setdefault(i, []).append(letter)
        else:
            new_false_letters.append(letter)
    
    false_letters.extend(new_false_letters)
    
    for position, letter in new_true_letters.items():
        if position not in true_letters:
            true_letters[position] = letter
    
    for position, letters in new_misplaced_letters.items():
        if position not in misplaced_letters:
            misplaced_letters[position] = []
        misplaced_letters[position].extend(letters)
            
    return list(set(false_letters)), true_letters, misplaced_letters



def guess_word(words, false_letters, true_letters, misplaced_letters, weighted = True):
    
    filtered_words = words
    
    for idx, letter in true_letters.items():
        filtered_words = filtered_words[filtered_words['words'].apply(lambda x: x[idx] == letter)]
    
    for letter in false_letters:
        filtered_words = filtered_words[~filtered_words['words'].str.contains(letter)]
    
    filtered_words = filtered_words[filtered_words['words'].apply(lambda word: all(letter in word and word[idx] != letter for idx, letter_list in misplaced_letters.items() for letter in letter_list))]
    
    filtered_words['words'] = shuffle(filtered_words['words'])

    if weighted:
        guess = random.choices(list(filtered_words['words']), weights = list(filtered_words['freq']))[0]
    else:
       guess = random.choice(list(filtered_words['words']))
    
    return guess, len(filtered_words)


def run(n = 1, weighted = True):
    
    game_details = {}
    
    for i in range(n):
        
        game_details[i] = {}
        game_details[i]['n_choices'] = []
        game_details[i]['guesses'] = []
        game_details[i]['feedback'] = {}
        
        if weighted:
            answer = random.choices(words['words'], weights = words['freq'])[0]
        else:
           answer = random.choice(list(words['words']))
        false_letters, true_letters, misplaced_letters, guess = [], {}, {}, None
        
        while guess != answer:  
            
            guess, num_choices = guess_word(words, false_letters, true_letters, misplaced_letters, weighted = (True if weighted else False))
            game_details[i]['n_choices'].append(num_choices)
            game_details[i]['guesses'].append(guess)
            
            false_letters, true_letters, misplaced_letters = check(answer, guess, false_letters, true_letters, misplaced_letters)
            game_details[i]['feedback']['false_letters'] = false_letters
            game_details[i]['feedback']['true_letters'] = true_letters
            game_details[i]['feedback']['misplaced_letters'] = misplaced_letters
            
        game_details[i]['n_tries'] = len(game_details[i]['guesses'])
        res = pd.DataFrame.from_dict(game_details).transpose()[['n_tries', 'n_choices','guesses', 'feedback']]
        res['won'] = 1
        res.loc[res['n_tries'] > 6, 'won'] = 0
        
    return res


def run_with_first_guess(first_guess, n = 1, weighted = True):
        
    game_details = {}
    
    for i in range(n):
        
        game_details[i] = {}
        game_details[i]['n_choices'] = []
        game_details[i]['guesses'] = []
        game_details[i]['feedback'] = {}

        if weighted:
            answer = random.choices(words['words'], weights = words['freq'])[0]
        else:
           answer = random.choice(list(words['words']))

        false_letters, true_letters, misplaced_letters, guess = [], {}, {}, first_guess
        game_details[i]['n_choices'].append(1)
        game_details[i]['guesses'].append(guess)
        false_letters, true_letters, misplaced_letters = check(answer, guess, false_letters, true_letters, misplaced_letters)
        game_details[i]['feedback']['false_letters'] = false_letters
        game_details[i]['feedback']['true_letters'] = true_letters
        game_details[i]['feedback']['misplaced_letters'] = misplaced_letters

        while guess != answer:  
        
            guess, num_choices = guess_word(words, false_letters, true_letters, misplaced_letters, weighted = (True if weighted else False))
            game_details[i]['n_choices'].append(num_choices)
            game_details[i]['guesses'].append(guess)
            
            false_letters, true_letters, misplaced_letters = check(answer, guess, false_letters, true_letters, misplaced_letters)
            game_details[i]['feedback']['false_letters'] = false_letters
            game_details[i]['feedback']['true_letters'] = true_letters
            game_details[i]['feedback']['misplaced_letters'] = misplaced_letters
            
        game_details[i]['n_tries'] = len(game_details[i]['guesses'])
        res = pd.DataFrame.from_dict(game_details).transpose()[['n_tries', 'n_choices','guesses', 'feedback']]
        res['won'] = 1
        res.loc[res['n_tries'] > 6, 'won'] = 0
        
    return res
            
def run_with_answer(answer, n = 1, weighted = True):
    
    game_details = {}
    
    for i in range(n):
        
        game_details[i] = {}
        game_details[i]['n_choices'] = []
        game_details[i]['guesses'] = []
        game_details[i]['feedback'] = {}
        
        false_letters, true_letters, misplaced_letters, guess = [], {}, {}, None
        
        while guess != answer:  
            
            guess, num_choices = guess_word(words, false_letters, true_letters, misplaced_letters, weighted = (True if weighted else False))
            game_details[i]['n_choices'].append(num_choices)
            game_details[i]['guesses'].append(guess)
            
            false_letters, true_letters, misplaced_letters = check(answer, guess, false_letters, true_letters, misplaced_letters)
            game_details[i]['feedback']['false_letters'] = false_letters
            game_details[i]['feedback']['true_letters'] = true_letters
            game_details[i]['feedback']['misplaced_letters'] = misplaced_letters
            
        game_details[i]['n_tries'] = len(game_details[i]['guesses'])
        res = pd.DataFrame.from_dict(game_details).transpose()[['n_tries', 'n_choices','guesses', 'feedback']]
        res['won'] = 1
        res.loc[res['n_tries'] > 6, 'won'] = 0
        
    return res

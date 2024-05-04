from simulator import run, run_with_first_guess, run_with_answer, words
import pandas as pd
import multiprocessing as mp

# run(n = 3000, weighted = True).to_csv('results/weighted.csv', index = None)
# run(n = 3000, weighted= False).to_csv('results/non_weighted.csv', index = None)


# optimal words
# result_optimal = pd.DataFrame()
# for i in range(len(words)):
#     res = run_with_first_guess(words.iloc[i]['words'], 100, weighted=True)
#     result_optimal = pd.concat([result_optimal, res])
#     print(i,len(words),round(i/len(words), 2), end = '\r')
# result_optimal.to_csv('results/optimal_word_raw.csv', index = None)

# difficulty_level
# result_difficulty = pd.DataFrame()
# for i in range(len(words)):
#     res = run_with_answer(answer = words.iloc[i]['words'], n = 100, weighted= True)
#     result_difficulty = pd.concat([result_difficulty, res])
#     print(i,len(words),round(i/len(words), 2), end = '\r')
# result_difficulty.to_csv('results/difficulty_level_raw.csv', index = None)


import random
from math import comb
import numpy as np


def p_k(p, n, k):
    return comb(3,k) * pow(p, k) * pow((1-p), (n-k))

if __name__ == '__main__':
    k_max_for_coin_one = 2

    choices_of_coins = ['one', 'two']
    weight_p = [3, 1]
    # weight_p = [0.75, 0.25]

    choices = ['H', 'T']
    # coin_weights = {
    #     'one': [0.25, 0.75],
    #     'two': [0.75, 0.25]
    # }
    coin_weights = {
        'one': [1, 3],
        'two': [3, 1]
    }

    total_guesses = 1
    correct_guesses = 0.0
    for i in range(0, total_guesses):
        
        picked_coin = random.choices(choices_of_coins, weights=weight_p, k=1)[0]
        # picked_coin = np.random.choice(choices_of_coins, p=weight_p)

        # print(picked_coin)

        flip_results = random.choices(choices, weights=coin_weights[picked_coin], k=3)
        # flip_results = np.random.choice(choices, size=3, p=coin_weights[picked_coin])


        # print(flip_results)

        number_of_heads = len([f for f in flip_results if f == 'H'])

        # print(number_of_heads)

        guess = 'one' if number_of_heads <= k_max_for_coin_one else 'two'

        # print(guess)
        guess_correct = guess == picked_coin
        if guess_correct:
            correct_guesses = correct_guesses + 1

        # print(correct_guesses)
    
    print("correct/total", correct_guesses/total_guesses)

    print("#####")
    
    p = 0.25
    n = 3
    coin_one = p_k(p, n, 0) + p_k(p, n, 1) + p_k(p, n, 2)
    coin_two = p_k(1-p, n, 3)

    print(0.75*coin_one + 0.25*coin_two)
    
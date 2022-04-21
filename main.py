from random import choice
import sys

ALLOWED_GUESSES = 6

ext = lambda s: "\033[0;32m" + s + "\033[0m"
ptl = lambda s: "\033[0;33m" + s + "\033[0m"
wrg = lambda s: "\033[2m" + s + "\033[0m"


def check_guess(guess, answer):
    res = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            res += ext(letter)
        elif letter in answer:
            res += ptl(letter)
        else:
            res += wrg(letter)
    return "".join(res)


def game(chosen_word, allowed_guesses):
    alry_gsd = []
    acm_res = []

    while True:
        while True:
            guess = input("? ")
            guess = guess.upper().strip()
            if guess in alry_gsd:
                print(
                    "%s is not a valid guess because it has already been res."
                    % guess
                )
            elif guess not in allowed_guesses:
                print("%s is not in the dictionary." % guess)
            else:
                break
        alry_gsd.append(guess)
        res = check_guess(guess, chosen_word)
        acm_res.append(res)

        print(*acm_res, sep="\n")
        if guess == chosen_word:
            print("Congrats!  %s is the correct word." % guess)
            break
        elif len(alry_gsd) == ALLOWED_GUESSES:
            print("You ran out of attempts.  The correct word is %s." % chosen_word)
            break


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("You must and must only give two arguments, that is, the filename of the solution list, followed by that of the allowed guesses list.")
        sys.exit(1)
    try:
        allowed_solutions = [w.strip().upper() for w in open(sys.argv[1], "r").readlines()]
        allowed_guesses = set([w.strip().upper() for w in open(sys.argv[2], "r").readlines()])
        allowed_guesses = allowed_guesses | set(allowed_solutions)
    except FileNotFoundError:
        print("%s does not exist, so I can't open the word list!" % sys.argv[1])
        sys.exit(2)
    chosen_word = choice(allowed_solutions)
    game(chosen_word, allowed_guesses)

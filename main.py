import random
import string
from curses import wrapper
import curses
import time


def main(stdsrc):
    # Init colors
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    _, width = stdsrc.getmaxyx()

    # Init letter window
    letter_win = curses.newwin(15, width - 6, 10, 3)

    stdsrc.clear()

    # Variables
    best_solutions = {}
    letters = string.ascii_lowercase
    letters += " "
    number = 0
    try_count = 0
    curr_y = 0
    curr_x = 0
    best_try = ""
    temp_best_try = ""
    chance = len(letters) ** len(to_find)

    stdsrc.addstr(2, 3, "-Information-")
    stdsrc.addstr(3, 3, "Found: no")
    stdsrc.addstr(4, 3, f"Searched: {to_find}")
    stdsrc.addstr(5, 3, f"Chance: {chance}:1")
    stdsrc.addstr(6, 3, f"Try     x")
    stdsrc.addstr(7, 3, f"Best try: x (x%)")
    stdsrc.addstr(8, 3, f"Runtime in seconds: x")
    stdsrc.addstr(9, 3, f"Letters/Second: x")
    stdsrc.addstr(10, 3, f"Expected time left: x seconds")
    stdsrc.addstr(32, 3, "Best Solutions:")
    stdsrc.refresh()

    # Set time reference point
    start_time = time.time()
    while True:
        if curr_x == width - 6:
            curr_x = 0
            curr_y += 1
        if curr_y == 15:
            curr_x = 0
            curr_y = 0

        try_count += 1

        curr_x += 1
        curr_letter = random.choice(letters)

        if number == len(to_find):
            best_solutions[to_find] = 1
            break

        if curr_letter == to_find[number]:
            stdsrc.addstr(15 + curr_y, 2 + curr_x, curr_letter, curses.color_pair(2))
            temp_best_try += curr_letter
            number += 1
            if temp_best_try != "":
                if temp_best_try not in best_solutions.keys():
                    best_solutions[temp_best_try] = 1
                else:
                    best_solutions[temp_best_try] += 1
        else:
            temp_best_try = ""
            stdsrc.addstr(15 + curr_y, 2 + curr_x, curr_letter, curses.color_pair(1))
            number = 0

        if len(temp_best_try) > len(best_try):
            best_try = temp_best_try
            temp_best_try = ""

        stdsrc.addstr(
            7, 3, f"Best try: {best_try} ({round(100 / len(to_find)*len(best_try))}%)"
        )
        letters_p_s = try_count / (time.time() - start_time)
        stdsrc.addstr(6, 3, f"Try     {try_count}")
        stdsrc.addstr(8, 3, f"Runtime in seconds: {round(time.time()-start_time, 2)}s")
        stdsrc.addstr(9, 3, f"Letters/Second: {round(letters_p_s)}")
        stdsrc.addstr(
            10,
            3,
            f"Expected time left: {round((chance / letters_p_s) - (time.time() - start_time), 2)} seconds                   ",
        )

        # Add best solutions to bottom of screen
        for i, item in enumerate(best_solutions.keys()):
            stdsrc.addstr(
                32 + 1 + i,
                3,
                f"\"{item}\": {' '*(len(to_find)-i)} {best_solutions[item]} {' '*(14-len(str(best_solutions[item])))} ({round(best_solutions[item]/try_count, 4)}% of tries)                ",
            )

        stdsrc.refresh()

    for i, item in enumerate(best_solutions.keys()):
        stdsrc.addstr(
            32 + 1 + i, 3, f"\"{item}\": {' '*(len(to_find)-i)} {best_solutions[item]}"
        )
    stdsrc.addstr(3, 3, "Found: yes  ")
    stdsrc.refresh()
    stdsrc.getch()
    return


if __name__ == "__main__":
    # Written by Jonathan F.
    # https://github.com/Jonathan357611/InfiniteMonkeyTheorem
    to_find = input(f"Word to search > ").lower()
    wrapper(main)

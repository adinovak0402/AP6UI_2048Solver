from game import *
import numpy as np
import copy as cp


# Heuristický solver pro 2048
# Cíl: Nahromadit čísla v levém dolním rohu

def evaluate_grid(grid):
    """
    Vyhodnocuje stav mřížky podle těchto kritérií:
    1. Priorita pro maximální čísla v levém dolním rohu.
    2. Snižující se hodnoty směrem od rohu.
    3. Minimalizace prázdných políček.
    """
    score = 0
    weights = np.array([[4, 3, 2, 1],
                        [5, 4, 3, 2],
                        [6, 5, 4, 3],
                        [7, 6, 5, 4]])
    score += np.sum(grid * weights)  # Upřednostnění vysokých hodnot v rohu
    score -= np.count_nonzero(grid == 0) * 10  # Penalizace za prázdná pole
    return score


# Možné směry tahu
directions = ['left', 'right', 'up', 'down']

# Inicializace hry
grid, score = new_game()

# Herní smyčka
for i in range(1000):
    best_move = None
    best_score = -float('inf')

    # Vyzkoušení všech možných tahů a jejich vyhodnocení
    for direction in directions:
        test_grid, test_score = cp.deepcopy(grid), score
        try:
            test_grid, test_score = play_2048(test_grid, direction, test_score)
            evaluation = evaluate_grid(test_grid)
            if evaluation > best_score:
                best_score = evaluation
                best_move = direction
        except RuntimeError as inst:
            if str(inst) == "GO":
                print("GAME OVER in", i + 1, "moves")
                break
            elif str(inst) == "WIN":
                print("WIN in", i + 1, "moves")
                break

    # Kontrola, jestli hra skončila
    if best_move is None:
        print("GAME OVER in", i + 1, "moves")
        break

    # Zahrajeme nejlepší tah
    try:
        grid, score = play_2048(grid, best_move, score)
    except RuntimeError as inst:
        if str(inst) == "GO":
            print("GAME OVER in", i + 1, "moves")
        elif str(inst) == "WIN":
            print("WIN in", i + 1, "moves")
        break

    # Pokud vyhraje, ukončíme hru
    if check_win(grid):
        print("WIN in", i + 1, "moves")
        break

# Výsledná mřížka a skóre
print_grid(grid, score)

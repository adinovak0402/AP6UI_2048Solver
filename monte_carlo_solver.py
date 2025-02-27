from game import *


# Monte Carlo simulace s daným počtem iterací a hloubkou prohledávání
def monte_carlo(its, depth=50):
    total = 0
    max = 0
    min = float('inf')
    win = 0
    lose = 0
    moves = 0
    max_tile_values = []
    consecutive_same_moves = 0

    # Spouští simulaci pro daný počet iterací
    for i in range(its):
        print(i)
        grid, score = new_game()
        last_best_move = None

        # Maximálně 3000 tahů na hru
        for _ in range(3000):
            best_move = find_best_move(grid, score, depth)

            # Kontrola, jestli se tah neopakuje příliš často
            if best_move == last_best_move:
                consecutive_same_moves += 1
            else:
                consecutive_same_moves = 0
            if consecutive_same_moves == 50:
                print("50 same moves")
                # Pokud se tah opakuje 50x, vybere náhodný tah
                best_move = np.random.choice(('right', 'up', 'down'))
                consecutive_same_moves = 0
            last_best_move = best_move
            moves = moves + 1

            # Hraje tah a kontroluje konec hry
            try:
                grid, score = play_2048(grid, best_move, score)
            except RuntimeError as inst:
                if str(inst) == "GO":
                    total += score
                    print(score, "lose", moves)
                    lose = lose + 1
                    # Aktualizace maximálního a minimálního skóre
                    if score > max:
                        max = score
                    if score < min:
                        min = score
                    break
                elif str(inst) == "WIN":
                    print_grid(grid, score)
                    total += score
                    print(score, "win", moves)
                    win = win + 1
                    if score > max:
                        max = score
                    break

            # Kontrola maximální hodnoty na mřížce
            max_tile = np.max(grid)
            if max_tile == 2048:
                print_grid(grid, score)
                win = win + 1
            max_tile_values.append(max_tile)

    # Výpočet statistik po skončení simulace
    max_tile_avg = np.mean(max_tile_values)
    print(f"Max score: {max}")
    print(f"Avg score: {total / its}")
    print(f"W/L: {win}/{lose - win}")
    print("Max tile avg value:", max_tile_avg)
    print("Max tile in a game:", np.max(max_tile_values))
    print("Avg moves per game:", moves / its)
    return grid, total, moves, max_tile_avg  # nebo vhodné proměnné k návratu


# Funkce pro nalezení nejlepšího tahu pomocí hloubkového prohledávání
def find_best_move(grid, score, depth):
    moves = ['left', 'right', 'up', 'down']
    scores = []

    # Vyhodnocuje skóre pro každý možný tah
    for move in moves:
        try:
            temp_grid, temp_score = cp.deepcopy(grid), score
            temp_grid, temp_score = play_2048(temp_grid, move, temp_score)

            # Rekurzivní volání pro prohloubení simulace
            if depth > 1:
                _, temp_score = monte_carlo_depth(temp_grid, temp_score, depth - 1)

            scores.append(temp_score)
        except RuntimeError as inst:
            # Ošetření koncových stavů hry
            if str(inst) == "GO":
                scores.append(0)
            elif str(inst) == "WIN":
                scores.append(1)

    # Výběr nejlepšího tahu na základě skóre
    best_move = moves[np.argmax(scores)]
    return best_move


# Rekurzivní funkce pro hloubkové prohledávání Monte Carlo simulace
def monte_carlo_depth(grid, score, depth):
    # Konec rekurze, pokud je dosaženo maximální hloubky
    if depth == 0:
        return grid, score

    moves = ['left', 'right', 'up', 'down']
    scores = []

    # Vyhodnocení skóre pro každý tah na dané hloubce
    for move in moves:
        try:
            temp_grid, temp_score = cp.deepcopy(grid), score
            temp_grid, temp_score = play_2048(temp_grid, move, temp_score)

            # Rekurzivní volání pro další úroveň hloubky
            _, temp_score = monte_carlo_depth(temp_grid, temp_score, depth - 1)
            scores.append(temp_score)
        except RuntimeError as inst:
            # Ošetření koncových stavů hry
            if str(inst) == "GO":
                scores.append(score)
            elif str(inst) == "WIN":
                scores.append(float('inf'))

    # Vrací nejlepší skóre na dané úrovni
    return grid, max(scores)

import time
import numpy as np
import monte_carlo_solver
from circle_solver import directions as circle_directions
from random_solver import play_2048
from game import *
import matplotlib.pyplot as plt


# Funkce pro generování grafů na základě statistik
def generate_graphs(statistics, solvers):
    metrics = [
        'Win Ratio',
        'Wins',
        'Average Score',
        'Max Score',
        'Min Score',
        'Average Max Tile',
        'Max Tile',
        'Average Moves'
    ]

    # Definování barev pro jednotlivé solvery
    colors = {
        'Monte Carlo Solver': '#1f77b4',  # Modrá
        'Circle Solver': '#2ca02c',  # Zelená
        'Random Solver': '#ff7f0e'  # Oranžová
    }

    # Generování grafu pro každou metriku
    for metric in metrics:
        plt.figure(figsize=(10, 6))

        # Shromažďování dat pro všechny solvery
        data = [statistics[solver][metric] for solver in solvers]
        bars = plt.bar(solvers, data, color=[colors[solver] for solver in solvers])

        # Přidání hodnot nad sloupce
        for bar in bars:
            yval = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                yval,
                round(yval, 2),
                ha='center', va='bottom'
            )

        plt.title(metric)
        plt.ylabel(metric)
        plt.grid(True, linestyle='--', alpha=0.5)

        # Přidání legendy
        plt.legend(solvers, loc='upper right')

        # Zobrazení grafu
        plt.show()


# Funkce pro spuštění Monte Carlo simulace
def run_monte_carlo(run_number):
    grid, score, move_count, duration = monte_carlo_solver.monte_carlo(run_number)

    return grid, score, move_count, duration


# Funkce pro spuštění Circle Solveru
def run_circle_solver():
    grid, score = new_game()
    move_count = 0
    start_time = time.time()

    # Cykluje směry v pořadí uloženém v circle_directions
    while True:
        direction = circle_directions[move_count % 4]
        try:
            grid, score = play_2048(grid, direction, score)
            move_count += 1
        except RuntimeError as inst:
            break

    end_time = time.time()
    return grid, score, move_count, end_time - start_time


# Funkce pro spuštění Random Solveru
def run_random_solver():
    grid, score = new_game()
    move_count = 0
    start_time = time.time()

    # Volí náhodný směr pro každý tah
    while True:
        direction = np.random.choice(['left', 'right', 'up', 'down'])
        try:
            grid, score = play_2048(grid, direction, score)
            move_count += 1
        except RuntimeError as inst:
            break

    end_time = time.time()
    return grid, score, move_count, end_time - start_time


# Funkce pro sběr statistik z více spuštění solveru
def collect_stats(runs, solver_function):
    scores = []
    max_tiles = []
    move_counts = []
    times = []

    # Provede několik běhů a shromažďuje data
    for run_number in range(1, runs + 1):  # Číslování runů
        # Předej run_number pouze Monte Carlo solveru
        if solver_function.__name__ == "run_monte_carlo":
            grid, score, move_count, duration = solver_function(run_number)
        else:
            grid, score, move_count, duration = solver_function()  # Ostatní bez argumentu

        scores.append(score)
        max_tiles.append(np.max(grid))
        move_counts.append(move_count)
        times.append(duration)

    return scores, max_tiles, move_counts, times


# Funkce pro tisk a uložení statistik
def print_statistics(solver_name, scores, max_tiles, move_counts, times, statistics):
    print(f"\n=== {solver_name} ===")
    wins = sum(1 for tile in max_tiles if tile >= 2048)
    total_games = len(max_tiles)
    win_ratio = wins / total_games

    # Výpis statistických údajů
    print(f"W/L: {wins}/{total_games} ({win_ratio:.2f})")
    print(f"Average Score: {np.mean(scores):.2f}")
    print(f"Max Score: {np.max(scores)}")
    print(f"Min Score: {np.min(scores)}")
    print(f"Average Max Tile: {np.mean(max_tiles):.2f}")
    print(f"Max Tile: {np.max(max_tiles)}")
    print(f"Average Moves: {np.mean(move_counts):.2f}")
    print(f"Average Time: {np.mean(times):.2f} s")

    # Uložení statistik pro generování grafů
    statistics[solver_name] = {
        'Win Ratio': win_ratio,
        'Wins': wins,
        'Average Score': np.mean(scores),
        'Max Score': np.max(scores),
        'Min Score': np.min(scores),
        'Average Max Tile': np.mean(max_tiles),
        'Max Tile': np.max(max_tiles),
        'Average Moves': np.mean(move_counts),
        'Average Time': np.mean(times)
    }


def main():
    runs = 30

    # Sběr statistik pro jednotlivé solvery
    monte_carlo_stats = collect_stats(runs, run_monte_carlo)
    print("Monte Carlo end")
    circle_stats = collect_stats(runs, run_circle_solver)
    print("CircleSolver end")
    random_stats = collect_stats(runs, run_random_solver)
    print("Random end")

    statistics = {}
    print_statistics("Monte Carlo Solver", *monte_carlo_stats, statistics)
    print_statistics("Circle Solver", *circle_stats, statistics)
    print_statistics("Random Solver", *random_stats, statistics)

    # Generování grafů na základě statistik
    generate_graphs(statistics, ['Monte Carlo Solver', 'Circle Solver', 'Random Solver'])


if __name__ == "__main__":
    main()

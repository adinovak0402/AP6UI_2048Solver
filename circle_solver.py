from game import *

# Circle direction solver (left → up → right → down)
directions = ['left', 'up', 'right', 'down']
grid, score = new_game()
move_count = 0
max_tile = 0

while True:
    direction = directions[move_count % 4]  # Cycle through the directions
    try:
        grid, score = play_2048(grid, direction, score)
        move_count += 1
        max_tile = max(max_tile, np.max(grid))
    except RuntimeError as inst:
        if(str(inst) == "GO"):
            print("GAME OVER in", move_count, "moves")
            break
        elif(str(inst) == "WIN"):
            print("WIN in", move_count, "moves")
            break

print("Max Tile: ", max_tile)
print_grid(grid, score)

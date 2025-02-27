from game import *

#Random direction solver
grid, score = new_game()
for i in range(1000):
    direction = np.random.choice(('left','right','up','down'))
    try:
        grid, score = play_2048(grid, direction, score)
    except RuntimeError as inst:
        if(str(inst)=="GO"):
            print("GAME OVER in ",(i+1)," moves")
        elif(str(inst)=="WIN"):
            print("WIN in ",(i+1)," moves")
        break
print_grid(grid, score)
from ui import Window, Cell
from maze import Maze

def main():
    num_rows = 15
    num_cols = 15
    margin = 100
    screen_x = 1000
    screen_y = 1000
    cell_size= (screen_x - 2 * margin) / num_cols

    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size, win)

    print("maze created")
    is_solveable = maze.solve()
    if not is_solveable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    win.wait_for_close()
main()

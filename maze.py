from tkinter import Tk, Canvas
from typing import Any
from ui import Cell
from collections import deque
import random
import time

class Maze:
    def __init__(self, x1, y1, rows, cols, cell_size, win=None, seed=None):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.rows = rows
        self.cols = cols
        self.cell_size_x = cell_size
        self.cell_size_y = cell_size
        self.win = win

        if seed:
            random.seed(seed)

        self.create_cells()
        self.break_entrance()
        self.dfs_break_walls(0, 0)
        self.reset_cells()

    # fills a cells list w lists of cells
    # once the matrix is populated, call draw_cell on each cell
    def create_cells(self):
        for i in range(self.cols):
            column_cells = []
            for j in range(self.rows):
                column_cells.append(Cell(self.win))
            self.cells.append(column_cells)

        for i in range(self.cols):
            for j in range(self.rows):
                self.draw_cell(i, j)

    # calculates the x/y position of cell based on the i j, cell size , and x y position of the maze
    def draw_cell(self, i, j):
        if self.win is None:
            return

        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y

        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        self.cells[i][j].draw(x1, y1, x2, y2)
        self.animate(0.02)

    def animate(self, speed):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(speed)
    
    # creating entrance
    def break_entrance(self):
        self.cells[0][0].top_wall = False
        self.draw_cell(0,0)
        self.cells[self.cols - 1][self.rows - 1].bot_wall = False
        self.draw_cell(self.cols - 1, self.rows - 1)

    def dfs_break_walls(self, i, j):
        # marks current cell as visited
        self.cells[i][j].visited = True
        
        #determining which neighboring cell to visit
        while True:
            # golds potential next cells to visit
            next_index_list = []

            # left
            if i > 0 and not self.cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.cols - 1 and not self.cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self.cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.rows - 1 and not self.cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            if len(next_index_list) == 0:
                self.draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # right
            if next_index[0] == i + 1:
                self.cells[i][j].right_wall = False
                self.cells[i + 1][j].left_wall = False
            # left
            if next_index[0] == i - 1:
                self.cells[i][j].left_wall = False
                self.cells[i - 1][j].right_wall = False
            # down
            if next_index[1] == j + 1:
                self.cells[i][j].bot_wall = False
                self.cells[i][j + 1].top_wall = False
            # up
            if next_index[1] == j - 1:
                self.cells[i][j].top_wall = False
                self.cells[i][j - 1].bot_wall = False

            self.dfs_break_walls(next_index[0], next_index[1])

    def reset_cells(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    def bfs_solve(self, i, j):
        self.animate(0.04)

        search_queue = deque()
        search_queue.append((0, 0))  
        self.cells[0][0].visited = True  

        previous = {(0,0): None}

        while search_queue:
            current_i, current_j = search_queue.popleft()

            # if goal is reached
            if current_i == self.cols - 1 and current_j == self.rows - 1:
                path = self.reconstruct_path(previous, (0,0), (current_i, current_j))
                return path

            # enqueue all unvisited children and draw progress
            for child_i, child_j in self.getChildren(current_i, current_j):
                child_cell = self.cells[child_i][child_j]
                if not child_cell.visited:
                    child_cell.visited = True
                    search_queue.append((child_i, child_j))

                    previous[(child_i, child_j)] = (current_i, current_j)

                    self.cells[current_i][current_j].draw_progress(child_cell)
                    self.animate(0.04)  

                    self.cells[current_i][current_j].draw_progress(child_cell, True)

        return False

    def reconstruct_path(self, previous, start, goal):
        current = goal
        path = []
        while current != start:  
            path.append(current)
            current = previous[current]
        path.append(start)  
        # path.reverse()  

        for i in range(len(path) - 1):
            current = path[i]
            next = path[i + 1]
            self.cells[current[0]][current[1]].draw_progress(self.cells[next[0]][next[1]])
            self.animate(0.02)

    def getChildren(self, i, j):
        children = []

        # Look right
        if i < self.cols - 1 and not self.cells[i][j].right_wall and not self.cells[i + 1][j].left_wall:
            children.append((i + 1, j))

        # Look left
        if i > 0 and not self.cells[i][j].left_wall and not self.cells[i - 1][j].right_wall:
            children.append((i - 1, j))

        # Look top
        if j > 0 and not self.cells[i][j].top_wall and not self.cells[i][j - 1].bot_wall:
            children.append((i, j - 1))

        # Look bottom
        if j < self.rows - 1 and not self.cells[i][j].bot_wall and not self.cells[i][j + 1].top_wall:
            children.append((i, j + 1))           

        return children

    # create the moves for the solution using a depth first search
    def solve(self):
        return self.bfs_solve(0,0)


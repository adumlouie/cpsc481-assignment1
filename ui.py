from tkinter import Tk, Canvas

# creating graphical window class
class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("my maze solver")
        self.canvas = Canvas(self.root, bg="white", height=height, width=width)
        self.canvas.grid()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # function for redrawing all grahics int he window
    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    # takes an instance of a line and fill color and calls draw()
    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    # sets the running var to true and calls redraw() while running state is true
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.running = False

# stores two coords
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# takes two points as inputs and saves them as members
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # takes a Canvas and fill color a draws a line between the two coords
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=3)
        canvas.grid()

# holds data about individual cells that keeps tracks of which walls it has and where it exists on the canvas, takes in win widget
class Cell:
    def __init__(self, win):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bot_wall = True
        self.win = win
        self.visited = False

    # draws itself to the canvas
    def draw(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        # if wall exists, draw wall
        if self.left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.win.draw_line(line, "white")

        if self.top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.win.draw_line(line, "white")

        if self.right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.win.draw_line(line, "white")
        if self.bot_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.win.draw_line(line, "white")

    # draws path between two cells
    def draw_progress(self, to_cell, undo=False):
        # x and y mid points
        # diff ifs for up down left right 
        x_midpoint = (self.x1 + self.x2) / 2
        y_midpoint = (self.y1 + self.y2) / 2

        to_cell_x_midpoint = (to_cell.x1 + to_cell.x2) / 2
        to_cell_y_midpoint = (to_cell.y1 + to_cell.y2) / 2

        fill_color = 'blue'
        if undo:
            fill_color = 'gray'

        # right to left
        if self.x1 > to_cell.x1:
            line = Line(Point(x_midpoint, y_midpoint), Point(self.x1, y_midpoint))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell_x_midpoint, to_cell_y_midpoint), Point(to_cell.x2, to_cell_y_midpoint))
            self.win.draw_line(line, fill_color)
        
        # left to right
        elif self.x1 < to_cell.x1:
            line = Line(Point(x_midpoint, y_midpoint), Point(self.x2, y_midpoint))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell_x_midpoint, to_cell_y_midpoint), Point(to_cell.x1, to_cell_y_midpoint))
            self.win.draw_line(line, fill_color)

        # top to bot
        elif self.y1 < to_cell.y1:
            line = Line(Point(x_midpoint, y_midpoint), Point(x_midpoint, self.y2))
            self.win.draw_line(line, fill_color)
            line = Line(Point(to_cell_x_midpoint, to_cell.y1), Point(to_cell_x_midpoint, to_cell_y_midpoint))
            self.win.draw_line(line, fill_color)

        # bot to top
        elif self.y1 > to_cell.y1:
            line = Line(Point(to_cell_x_midpoint, to_cell_y_midpoint), Point(to_cell_x_midpoint, to_cell.y2))
            self.win.draw_line(line, fill_color)
            line = Line(Point(x_midpoint, self.y1), Point(x_midpoint, y_midpoint))
            self.win.draw_line(line, fill_color)


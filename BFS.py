# from graph import Graph
import collections
# from setup import *
#turtorial: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
#grid generation:
height_grid = 5
width_grid = 5
MARGIN = 0
# WIDTH = 1900
# HEIGHT = 1500
WIDTH = 1000
HEIGHT = 1000
rows = HEIGHT // height_grid #=15 (if i wanna change this later it makes it easy)
collombs  = WIDTH // width_grid #= 19
def _new_grid():
    grid = []
    for row in range(rows): # Add an empty array that will hold each cell in this row
        grid.append([])
        for column in range(collombs):
            grid[row].append(0)
    return grid

class SEARCH():
    def __init__(self):
        self.goal = "*"
        self.wall = "1"
        self.clear = "0"
        # self.grid = []  #2 dementional array


    def return_grid(self, goal):
        # Change the x/y player coordinates to grid coordinates
        # removing the old goal
        # old_goal = goal
        # column =old_goal[0] // (width_grid + MARGIN)
        # row = old_goal[1] // (height_grid + MARGIN)
        # self.grid[row][column] = "0"
        self.grid = _new_grid()
        column = goal[0] // (width_grid + MARGIN)
        row = goal[1] // (height_grid + MARGIN)
        # print(" the row and collomb",row, column)
        self.grid[row][column] = "*"  # Set that location to goal
        # print(self.grid)

        return self.grid

    def update_bfs(self, goal, start):   # these are player and zombies cordinates

        self.grid = self.return_grid(goal)
        column = start[0] // (width_grid + MARGIN)
        row = start[1] // (height_grid + MARGIN)
        start = (column, row)
        # Looks at all posiible branches to find the path aka get to goal
        queue = collections.deque([[start]])
        seen = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.grid[y][x] == self.goal:   # goal is an x and y cordinate for noww...
                # print(list(map(lambda x: (x[0]*width_grid, x[1]*height_grid), path)))
                return list(map(lambda x: (x[0]*width_grid, x[1]*height_grid), path)) # convet back into screen cordinates
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < collombs and 0 <= y2 < rows and \
                           self.grid[y2][x2] != self.wall and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
#
# # testing below
# goal = (1000,1000)    #player position
# start = (1000,0)     # zombie position
# test= SEARCH()    # SEACRCING class
# path = test.update_bfs(goal, start)  # returns the path that the zombi must take on the grid
# print("this is the path ", path)

import collections

# this is where the grid method was learned from:
# turtorial: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids

# grid generation:
height_grid = 5     # This is also set as the zombie speed
width_grid = 5
MARGIN = 0
WIDTH = 1000
HEIGHT = 1000
rows = HEIGHT // height_grid
collombs = WIDTH // width_grid

def _new_grid():
    grid = []
    for row in range(rows):         # Add an empty array that will hold each cell in this row
        grid.append([])
        for column in range(collombs):
            grid[row].append(0)
    return grid

class SEARCH():
    def __init__(self):
        self.goal = "*"
        self.wall = "0"      # no walls where implemented :(

    def return_grid(self, goal):

        self.grid = _new_grid()
        column = goal[0] // (width_grid + MARGIN)
        row = goal[1] // (height_grid + MARGIN)

        self.grid[row][column] = self.goal        # Set that player location to goal

        return self.grid

    def update_bfs(self, goal, start):      # these are player and zombies cordinates

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

            if self.grid[y][x] == self.goal:
                 # convet back into screen cordinates and return
                return list(map(lambda x: (x[0]*width_grid, x[1]*height_grid), path))

            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):

                if 0 <= x2 < collombs and 0 <= y2 < rows and \
                           self.grid[y2][x2] != self.wall and (x2, y2) not in seen:

                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

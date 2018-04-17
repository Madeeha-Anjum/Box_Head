import collections
def bfs(grid, start):
    print(type(start))
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]  #making the start point  be in the path
        if grid[y][x] == goal:
            return path    # the final path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < collombs and 0 <= y2 < rows  and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

wall, clear, goal = "#", ".", "*"
collombs, rows = 10, 5  #one more than the grid becase its indexed by 0
grid = ["..........",
        "...#*..##.",
        "..##...#..",
        ".....###..",
        ".........."]
print("length of test grid",len(grid))
print(grid[2][5])
print(grid[2][4])
print(grid[3][4])
print(grid[4][4])
print(grid[4][5])


# should be total 15 rows
# #grid =  [ ["symboles "]
#            ["symboles"]
#            ["symboles"]
#            ["symboles"]   ]
# if we have objects in areas we need to change the grid
# values to 1 where ever thoses object are located in the grid
# thinking about doing pre programed grids in a text file
#and using arg to have the user chose the layout

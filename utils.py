def get_square_3x3(grid, row, column):
    square = []
    if row<3:
        if column < 3:
            square = [grid[i][0:3] for i in range(0, 3)]
        elif column<6:
            square = [grid[i][3:6] for i in range(0, 3)]
        else:  
            square = [grid[i][6:9] for i in range(0, 3)]
    elif row<6:
        if column < 3:
            square=[grid[i][0:3] for i in range(3,6)]
        elif column < 6:
            square = [grid[i][3:6] for i in range(3,6)]
        else:  
            square=[grid[i][6:9] for i in range(3,6)]
    else:
        if column < 3:
            square = [grid[i][0:3] for i in range(6,9)]
        elif column < 6:
            square = [grid[i][3:6] for i in range(6,9)]
        else:  
            square = [grid[i][6:9] for i in range(6,9)]
    return square
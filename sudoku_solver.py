from utils import get_square_3x3

class SudokuSolver():
    
    def __init__(self, board):
        self.board = board

    def __find_empty(self):
        for i in range(0,81):
            row = i // 9
            column = i % 9
            if self.board[row][column] == 0:
                return (row, column)  # row, col

        return None
    
    @classmethod
    def check_grid(cls, grid):
        for i in range(0, 81):
            row = i // 9
            column = i % 9
            if grid[row][column] == 0:
                return False
        return True

    def solve(self):
        find = self.__find_empty()
        if not find:
            return True
        else:
            row, column = find

        for i in range(1,10):
            if self.__valid(i, (row, column)):
                self.board[row][column] = i

                if self.solve():
                    return True

                self.board[row][column] = 0

        return False

    # @classmethod
    # def fill_solve(cls, grid):
    #     global counter
    #     for i in range(0,81):
    #         row = i // 9
    #         column = i % 9
    #         if grid[row][column]==0:
    #             for value in range (1,10):
    #                 #Check that this value has not already be used on this row
    #                 if not(value in grid[row]):
    #                 #Check that this value has not already be used on this column
    #                     if not value in (grid[0][column], grid[1][column], grid[2][column], grid[3][column], grid[4][column], grid[5][column], grid[6][column], grid[7][column], grid[8][column]):
    #                     #Identify which of the 9 squares we are working on
    #                         square = get_square_3x3(grid, row, column)
    #                         if not value in (square[0] + square[1] + square[2]):
    #                             grid[row][column]=value
    #                             if cls.__check_grid(grid):
    #                                 counter += 1
    #                                 break
    #                             else:
    #                                 if cls.fill_solve(grid):
    #                                     return grid
    #             break
    #     grid[row][column]=0
    #     return grid

    def __valid(self, num, pos):
        # num is current value
        # pos is position of num (row, column)
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if self.board[i][j] == num and (i,j) != pos:
                    return False

        return True
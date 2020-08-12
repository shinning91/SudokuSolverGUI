class SudokuSolver():
    
    def __init__(self, board):
        self.board = board

    def __find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j])
                if self.board[i][j] == 0:
                    print(i)
                    print(j)
                    return (i, j)  # row, col

        return None

    def solve(self):
        find = self.__find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.__valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False


    def __valid(self, num, pos):
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
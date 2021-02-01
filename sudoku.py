import argparse

from random import randint, shuffle
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

from sudoku_solver import SudokuSolver
from utils import get_square_3x3

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
counter = 0 # Counter for number of solutions


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            required=False)

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    return args['board']


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.left_frame = Frame(self, width=WIDTH+50, height=HEIGHT+50, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        self.right_frame = Frame(self, width=200, height=HEIGHT+50, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)
        self.canvas = Canvas(self.left_frame,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(
            self.right_frame,
            text="Clear answers",
            width=15,
            height=2,
            command=self.__clear_answers,
            highlightbackground='#3E4149'
        )
        clear_button.pack(fill=BOTH, side=BOTTOM)
        auto_solve_button = Button(
            self.right_frame,
            text="Solve puzzle",
            width=15,
            height=2,
            command=self.__solve_puzzle,
            highlightbackground='#3E4149'
        )
        auto_solve_button.pack(fill=BOTH, side=BOTTOM)
        generate_puzzle_button = Button(
            self.right_frame,
            text="Generate new puzzle",
            width=15,
            height=2,
            command=self.__generate_puzzle,
            highlightbackground='#3E4149'
        )
        generate_puzzle_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()
    
    def __solve_puzzle(self):
        solver = SudokuSolver(self.game.puzzle)
        solver.solve()
        self.__draw_puzzle()

    def __generate_puzzle(self):
        self.game.start_puzzle = SudokuBoard.create_empty_board()
        self.game.generate_puzzle(self.game.start_puzzle)
        self.game.start()
        self.__draw_puzzle()

    def __undo_move(self):
        self.move_stack = []

    def __erase_cell(self):
        print("ERASE");


class SudokuBoard(object):
    """
    Sudoku Board representation
    Represent sudoku board values
    """
    def __init__(self, board=None, board_file=None):
        if board_file:
            self.board = self.__create_board(board_file=board_file)
        else:
            self.board = self.__create_board(board=board)

    def __create_board(self, board=[], board_file=None):
        board = []
        if board_file:
            for line in board_file:
                line = line.strip()
                if len(line) != 9:
                    raise SudokuError(
                        "Each line in the sudoku puzzle must be 9 chars long."
                    )
                board.append([])

                for c in line:
                    if not c.isdigit():
                        raise SudokuError(
                            "Valid characters for a sudoku puzzle must be in 0-9"
                        )
                    board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board

    @classmethod
    def create_empty_board(self):
        board = []
        for line in range(9):
            board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """

    def __init__(self, board=None, board_file=None):
        self.number_list = [1,2,3,4,5,6,7,8,9]
        if board_file:
            self.start_puzzle = SudokuBoard(board_file=board_file).board
        elif board:
            self.start_puzzle = SudokuBoard(board=board).board
        else:
            self.generate_puzzle(SudokuBoard.create_empty_board())

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def generate_puzzle(self, puzzle):
        self.__fill_grid(puzzle)
        self.__remove_random_grid_values()

    def __check_block(self, block):
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )

    def __check_grid(self, grid):
        for row in range(0,9):
            for col in range(0,9):
                if grid[row][col]==0:
                    return False

        #We have a complete grid!  
        return True 

    def __fill_grid(self, grid):
        #Find next empty cell
        for i in range(0, 81):
            row = i // 9
            column = i % 9
            if grid[row][column] == 0:
                shuffle(self.number_list)      
                for value in self.number_list:
                    #Check that this value has not already be used on this row
                    if not(value in grid[row]):
                        #Check that this value has not already be used on this column
                        if not value in (grid[0][column], grid[1][column], grid[2][column], grid[3][column], grid[4][column], grid[5][column], grid[6][column], grid[7][column], grid[8][column]):
                            #Identify which of the 9 squares we are working on
                            # E.g.
                            # square = [
                            #           [1][2][3],
                            #           [4][5][6],
                            #           [7][8][9]
                            #          ]
                            square = get_square_3x3(grid, row, column)
                            #Check that this value has not already be used on this 3x3 square
                            #Square contains 3 list of array of values for each row
                            if not value in (square[0] + square[1] + square[2]):
                                grid[row][column] = value
                                if self.__check_grid(grid):
                                    return True
                                else:
                                    if self.__fill_grid(grid):
                                        return True
                break
        grid[row][column]=0
        self.start_puzzle = grid

    def __remove_random_grid_values(self):
        global counter
        grid = self.start_puzzle
        row = randint(0, 8)
        column = randint(0, 8)

        attempts = 5 # Number of attemps trying new position when multiple solution found
        
        # Remove values from grid until all attempts used
        while attempts>0:
            while grid[row][column] == 0:
                row = randint(0, 8)
                column = randint(0, 8)
            
            backup = grid[row][column]
            grid[row][column] = 0
            copy_grid = []
            for r in range(0,9):
                copy_grid.append([])
                for c in range(0,9):
                    copy_grid[r].append(grid[r][c])
            counter = 0
            self.fill_solve(copy_grid)

            # If counter > 1 means multiple solution found
            if counter!=1:
                grid[row][column]=backup
                attempts -= 1


        # print(grid)
        self.start_puzzle = grid

    def fill_solve(self, grid):
        global counter
        for i in range(0,81):
            row = i // 9
            column = i % 9
            if grid[row][column]==0:
                for value in range (1,10):
                    #Check that this value has not already be used on this row
                    if not(value in grid[row]):
                    #Check that this value has not already be used on this column
                        if not value in (grid[0][column], grid[1][column], grid[2][column], grid[3][column], grid[4][column], grid[5][column], grid[6][column], grid[7][column], grid[8][column]):
                        #Identify which of the 9 squares we are working on
                            square = get_square_3x3(grid, row, column)
                            if not value in (square[0] + square[1] + square[2]):
                                grid[row][column]=value
                                if SudokuSolver.check_grid(grid):
                                    counter += 1
                                    break
                                else:
                                    if self.fill_solve(grid):
                                        return True
                break
        grid[row][column]=0


if __name__ == '__main__':
    board_name = parse_arguments()
    game = SudokuGame()
    if board_name:
        with open('%s.sudoku' % board_name, 'r') as board_file:
            game = SudokuGame(board_file=board_file)

    game.start()

    root = Tk()
    SudokuUI(root, game)
    root.geometry("%dx%d" % (WIDTH*1.6, HEIGHT + 80))
    root.mainloop()
    
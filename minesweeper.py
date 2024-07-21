import random
import re

class board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Creating the Board
        self.board = self.make_new_board()
        self.assign_values_to_board()
        # Keeping track of which locations have been uncovered
        # (row, col) touples saved into this set
        self.dug = set()
    
    def make_new_board(self):
        # Board based on dim_size and num_bombs
        # Constructing list of lists
        board = [[None for x in range(self.dim_size)] for x in range(self.dim_size)]


        # Planting the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size 
            col = loc % self.dim_size

            if board[row][col] == '*':
                continue
            board[row][col] = '*'
            bombs_planted += 1
        return board
    
    def assign_values_to_board(self):
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if self.board[row][col] == '*':
                    continue
                self.board[row][col] = self.get_num_neighboring_bombs(row, col)

    def get_num_neighboring_bombs(self, row, col):
        num = 0
        for r in range(max(0, row-1), min(self.dim_size, (row + 1) + 1)):
            for c in range(max(0, col-1), min(self.dim_size, (col + 1) + 1)):
                if r == row and c == col:
                    continue 
                if self.board[r][c] == '*':
                    num += 1
        return num
        
    def dig(self, row, col):
        # Step 1: Dig at that location
            # Hit a bomb -> Over
            # Neighboring bombs -> Finish Dig
            # No Neighboring bombs -> Keep Digging in all areas
        # Step 2a: Return True if succesful
        # Step 2b: Return False if unsuccesful
        self.dug.add((row,col))
        if self.board[row][col] == '*':
            return False
        elif int(self.board[row][col]) > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        
        visible_board = [[None for x in range(self.dim_size)] for x in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # Put it all into a String
        # Simple .join method
        # list = [str(x) for x in visible_board]
        # return ''.join(list)
    
        # More advanced way

        string_rep = ''
        # Get max column width for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(max(columns, key = len))
        
        # Print the csv strings

        indices = [x for x in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep 



    

def play(dim_size = 10, num_bombs = 10):
    # Step 1: Create board and plant bombs
    Board = board(dim_size, num_bombs)
    # Step 2: Show board and ask where to dig
    # Step 3a: If location is a bomb, game over
    # Step 3b: If it's not a bomb, dig recursivly until you reach a square next to a bomb
    # Step 4: Repeat steps 2 and 3 until there are no more places to dig
    safe = True
    while len(Board.dug) < dim_size**2 - num_bombs:
        print(Board)
        user_input = re.split(',(\\s)*', input('Where would you like to play? Input in the form row, col: '))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
            print('Invalid location. Try again.')
            continue
        safe = Board.dig(row, col)
        if not safe:
            break
    if safe:
        print('Congratulations! You are victorious')
    else:
        print('GAME OVER')
        Board.dug  = [(r, c) for r in range(dim_size) for c in range(dim_size)]
        print(Board)

if __name__ == '__main__':
    play()




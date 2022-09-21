import random
import re

class Board:
    def __init__(self, board_size, bomb_amount):
        self.board_size = board_size
        self.bomb_amount = bomb_amount
        
        # The board!
        self.board = self.make_new_board()
        self.assign_values_to_board()
        
        print(self.board)
        print(bomb_amount)
        
        # Keeps track of which locations we have already uncovered
        self.dug = set()
    
    # Generates a new board of size field_size x field_size
    # We'll use list of lists to represent the board
    def make_new_board(self):
        
        # Creates a square array of "None"
        board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Plant the bombs
        planted_bombs = 0
        while planted_bombs < self.bomb_amount:
            
            # Returns a random integer that is within our square field
            location = random.randint(0, self.board_size**2 - 1)
            row = location // self.board_size
            column = location % self.board_size
            
            # Checks whether [row, column] already has a bomb
            if board[row][column] == "*":
                continue
        
            # Otherwise, plant the bomb
            board[row][column] = "*"
            planted_bombs += 1
            
        return board    
    
    # Assigns a number for all empty spaces, which represents how many neighboring bombs there are
    def assign_values_to_board(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                
                # If it's already a bomb... skip it!
                if self.board[row][column] == "*":
                    continue
                
                self.board[row][column] = self.get_num_neighboring_bombs(row, column)
    
    # Iterate through every neighboring prositinos and sum bombs    
    def get_num_neighboring_bombs(self, row, column):
        hits = 0
        
        # Adding min and max to avoid going out of bounds
        for r in range(max(0, row - 1), min(self.board_size - 1, row + 1) + 1):
            for c in range(max(0, column - 1), min(self.board_size - 1, column + 1) + 1):
                
                # This is our location and does not need to be checked
                if r == row and c == column:
                    continue
                if self.board[r][c] == "*":
                    hits += 1
                    
        return hits
    
    # Digs at location!
    def dig(self, row, column):
        
        # Keep track where exactly we dug
        self.dug.add((row, column))
        
        # Get rekt! Otherwise...
        if self.board[row][column] == "*":
            return False
        
        # Checks for bombs nearby! Otherwise...
        elif self.board[row][column] > 0:
            return True
    
        # Recursively dig everything!
        for r in range(max(0, row - 1), min(self.board_size - 1, row + 1) + 1):
            for c in range(max(0, column - 1), min(self.board_size - 1, column + 1) + 1):
                
                # Don't dig where we have already dug!
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
                
        return True

    # It will print whatever this function returns. Poggers?
    def __str__(self):
        
        # Create the string representation for the board:
        string_representation = ""
        
        for row in range(self.board_size):
            
            if row == 0:
                continue
            string_representation += "\n"
            
            for column in range(self.board_size):
                
                if (row, column) in self.dug:
                    string_representation += "  {}  ".format(str(self.board[row][column]))
                else:
                    string_representation += " {} ".format(" - ")
        
        return string_representation
        
# Play the game!
def play(board_size = 8, bomb_amount = 8):
    # Step 1: create the board
    # Step 2: plant the bombs
    board = Board(board_size, bomb_amount)
    
    # Step 3a: if the location is a bomb, show "Game over!" message
    # Step 3b: otherwise, dig recursivel until each square is at least next to a bomb
    # Step 4: repeat steps 2 and 3 until there are no more places to dig
    
    safe = True
    
    while len(board.dug) < board.board_size ** 2 - bomb_amount:
        print(board)
        
        # Uses regular expressions (regex) to parse the string and accept "x,x", "x, x" and "x,        x"
        user_input = re.split(",(\\s)*", input("Where would you like to dig? (x, y): "))
        row, column = int(user_input[0]), int(user_input[-1])
        
        if row < 0 or row >= board.board_size or column < 0 or column >= board.board_size:
            print("Invalid location!")
            continue
        
        # Dig if valid
        safe = board.dig(row, column)
        if not safe:
            # Shit!
            break
        
    if safe:
        print("GG ez")
    else:
        print("Get rekt, noob")
        board.dug = [(r, c) for r in range(board.board_size) for c in range(board.board_size)]

    print(board)
        
if  __name__ == "__main__":
    play()
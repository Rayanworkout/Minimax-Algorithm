class TicTacToe:
    
    def __init__(self, lines: int = 3, columns: int = 3) -> None:
        self.lines = lines
        self.columns = columns

        self.username = input("Hello, what's your name ?\n").strip()
        self.user_symbol = input('Choose a symbol between "X" and "O".\n').upper()
        
        while self.user_symbol not in ["O", "X"]:
            print("Your symbol need to be either O or X.")
            self.user_symbol = input('Choose a symbol between "X" and "O".\n').upper()

        self.computer_symbol = "X" if self.user_symbol == "O" else "O"

        self.grid = [["_"] * self.columns for _ in range(self.lines)]

        print(f"Hello {self.username}, your symbol is {self.user_symbol}.\n")
        print("How to play ?")
        print("You need to enter the line and the column on which you want to play. We start indexes from 1.")
        print('Example: "1, 3" to play on line 1, column 3.\n')

    def __str__(self) -> str:
        string_rep = ""
        for line in self.grid:
            string_rep += f"{line}\n"

        return string_rep


    def __is_full(self):
        return "_" not in [column for line in self.grid for column in line]


    def __check_win(self, grid):
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != "_":
                return grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] != "_":
                return grid[0][i]

        if grid[0][0] == grid[1][1] == grid[2][2] != "_":
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != "_":
            return grid[0][2]

        return None

    def __best_move(self):
        best_score = -float('inf')

        move = (-1, -1)
        
        for row in range(self.lines):
            for col in range(self.columns):
                if self.grid[row][col] == "_":
                    self.grid[row][col] = self.computer_symbol
                    score = self.__minimax(self.grid, 0, False)
                    self.grid[row][col] = "_"
                    
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        
        if move != (-1, -1):
            return move
        
        return None
    
    def __minimax(self, board, depth, is_maximizing):
        result = self.__check_win(board)
        if result:
            if result == self.computer_symbol:
                return 10 - depth
            elif result == self.user_symbol:
                return depth - 10
            else:
                return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for row in range(self.lines):
                for col in range(self.columns):
                    if board[row][col] == "_":
                        board[row][col] = self.computer_symbol
                        score = self.__minimax(board, depth + 1, False)
                        board[row][col] = "_"
                        best_score = max(score, best_score)

            return best_score
        else:
            best_score = float('inf')
            for row in range(self.lines):
                for col in range(self.columns):
                    if board[row][col] == "_":
                        board[row][col] = self.user_symbol
                        score = self.__minimax(board, depth + 1, True)
                        board[row][col] = "_"
                        best_score = min(score, best_score)

            return best_score

    
    def play(self, line: int = None, column: int = None, computer=False):
        line -= 1
        column -= 1

        if computer:
            print(f">> Computer plays on line {line + 1}, column {column + 1}.")
            self.grid[line][column] = self.computer_symbol
        else:
            if line is None or column is None:
                raise ValueError("You need to pass a line number and a column number.")

            if self.grid[line][column] == "_":
                print(f">> {self.username} plays on line {line + 1}, column {column + 1}.")
                self.grid[line][column] = self.user_symbol
            else:
                print("You cannot play here.")
                return

        # Check winner
        winner = self.__check_win(self.grid)
        if winner:
            print(f"{winner} wins!")
            print(self)
            exit(0)

        if self.__is_full():
            print("Board is full! It's a tie!")
            print(self)
            exit(0)

        if not computer:
            # Make computer play
            move = self.__best_move()
            if move:
                self.play(move[0] + 1, move[1] + 1, computer=True)
            print(self)
                
    def run(self):
        print(self)
        while True:
            try:
                line, column = (
                input("Enter a line and a column to play, comma separated !\n")
                .strip()
                .split(",")
            )
                line = int(line)
                column = int(column)
                
                if line > self.lines or column > self.columns:
                    print("Invalid values !")
                    continue
                else:
                    self.play(line, column)
            except (ValueError):
                continue


try:
    game = TicTacToe()
    game.run()
    
except KeyboardInterrupt:
    print("\nExiting game ...")
    exit(0)

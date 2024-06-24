import curses

class TicTacToe:
    def __init__(self, lines: int = 3, columns: int = 3) -> None:
        self.lines = lines
        self.columns = columns
        self.username = ""
        self.user_symbol = ""
        self.computer_symbol = ""
        self.grid = [["_"] * self.columns for _ in range(self.lines)]
        self.screen = None
        self.cursor = [0, 0]
    
    def setup_game(self):
        curses.echo()
        self.screen.addstr(0, 0, "Hello, what's your name?\n\nName : ")
        self.username = self.screen.getstr().decode('utf-8').strip()
        self.screen.clear()
        
        self.screen.addstr(1, 0, 'Choose a symbol between "X" and "O".\nSymbol : ')
        self.user_symbol = self.screen.getstr().decode('utf-8').upper().strip()
        
        while self.user_symbol not in ["O", "X"]:
            self.screen.addstr(2, 0, "Your symbol needs to be either O or X.")
            self.user_symbol = self.screen.getstr().decode('utf-8').upper().strip()
        
        self.computer_symbol = "X" if self.user_symbol == "O" else "O"
        
        self.screen.clear()
        self.screen.addstr(0, 0, f"Hello {self.username}, your symbol is {self.user_symbol}.\n")
        self.screen.addstr(1, 0, "How to play?")
        self.screen.addstr(2, 0, "Use arrow keys to move, and press Enter to select.\n")
        self.screen.refresh()
    
    def __str__(self) -> str:
        string_rep = ""
        for line in self.grid:
            string_rep += " | ".join(line) + "\n"
        return string_rep
    
    def draw_board(self):
        self.screen.clear()
        for i, line in enumerate(self.grid):
            self.screen.addstr(i * 2, 0, " | ".join(line))
            if i < self.lines - 1:
                self.screen.addstr(i * 2 + 1, 0, "---+---+---")
        
        self.screen.addstr(self.lines * 2, 0, "Use arrow keys to move, and press Enter to select.")
        self.screen.refresh()
    
    def __is_full(self) -> bool:
        return "_" not in [cell for row in self.grid for cell in row]
    
    def __check_win(self):
        for i in range(self.lines):
            if all(self.grid[i][j] == self.grid[i][0] != "_" for j in range(self.columns)):
                return self.grid[i][0]
            if all(self.grid[j][i] == self.grid[0][i] != "_" for j in range(self.lines)):
                return self.grid[0][i]
        
        if all(self.grid[i][i] == self.grid[0][0] != "_" for i in range(self.lines)):
            return self.grid[0][0]
        if all(self.grid[i][self.columns - 1 - i] == self.grid[0][self.columns - 1] != "_" for i in range(self.lines)):
            return self.grid[0][self.columns - 1]
        
        return None
    
    def __best_move(self) -> tuple:
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
        
        return move
    
    def __minimax(self, board, depth, is_maximizing) -> int:
        result = self.__check_win()
        if result:
            if result == self.computer_symbol:
                return 10 - depth
            elif result == self.user_symbol:
                return depth - 10
            else:
                return 0
        
        if self.__is_full():
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
    
    def play(self, line: int = None, column: int = None, computer: bool = False) -> None:
        if line is None or column is None:
            raise ValueError("You need to pass a line number and a column number.")
        
        line -= 1
        column -= 1
        
        if computer:
            self.grid[line][column] = self.computer_symbol
        else:
            if self.grid[line][column] == "_":
                self.grid[line][column] = self.user_symbol
            else:
                return
        
        self.draw_board()
        
        winner = self.__check_win()
        if winner:
            self.screen.addstr(self.lines * 3, 0, f"{winner} wins!")
            self.screen.refresh()
            curses.napms(2000)
            exit(0)
        
        if self.__is_full():
            self.screen.addstr(self.lines * 3, 0, "Board is full! It's a tie!")
            self.screen.refresh()
            curses.napms(2000)
            exit(0)
        
        if not computer:
            move = self.__best_move()
            if move:
                self.play(move[0] + 1, move[1] + 1, computer=True)
    
    def run(self) -> None:
        self.screen = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(True)
        self.setup_game()
        self.draw_board()
        
        while True:
            try:
                key = self.screen.getch()
                if key == 27:  # ESC key
                    break
                elif key == curses.KEY_UP and self.cursor[0] > 0:
                    self.cursor[0] -= 1
                elif key == curses.KEY_DOWN and self.cursor[0] < self.lines - 1:
                    self.cursor[0] += 1
                elif key == curses.KEY_LEFT and self.cursor[1] > 0:
                    self.cursor[1] -= 1
                elif key == curses.KEY_RIGHT and self.cursor[1] < self.columns - 1:
                    self.cursor[1] += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    self.play(self.cursor[0] + 1, self.cursor[1] + 1)
                
                self.screen.move(self.cursor[0] * 2, self.cursor[1] * 4)
                self.screen.refresh()
            except KeyboardInterrupt:
                break
        
        self.cleanup()
    
    def cleanup(self):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

try:
    game = TicTacToe()
    curses.wrapper(game.run())
except KeyboardInterrupt:
    game.cleanup()
    print("\nExiting game ...")
    exit(0)
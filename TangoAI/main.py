import tkinter as tk
import random

# Constants
SUN = '☀️'
MOON = '🌑'
UNKNOWN = '❓'

class TangoPuzzle:
    def __init__(self, size):
        self.N = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.equals = []      # List of tuples: [((r1, c1), (r2, c2)), ...]
        self.notequals = []   # Same, but for '≠'
        self.window = tk.Tk()
        self.window.title(f"Tango Puzzle - {self.N}x{self.N}")
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

    def print_grid(self):
        for row in self.grid:
            print(' '.join(['☀️' if cell == 'S' else '🌑' if cell == 'M' else '❓' for cell in row]))

    def update_grid_display(self):
        for r in range(self.N):
            for c in range(self.N):
                symbol = self.grid[r][c]
                if symbol is None:
                    symbol = UNKNOWN
                self.buttons[r][c].config(text=symbol)

    def is_valid(self, row, col, symbol):
        # Row balance constraint: no more than N//2 of the same type in a row
        row_vals = [v for v in self.grid[row] if v]
        if row_vals.count(symbol) > self.N // 2:
            return False

        # Column balance constraint: no more than N//2 of the same type in a column
        col_vals = [self.grid[r][col] for r in range(self.N) if self.grid[r][col]]
        if col_vals.count(symbol) > self.N // 2:
            return False

        # Check for more than two identical symbols in a row
        if col >= 2 and self.grid[row][col-1] == self.grid[row][col-2] == symbol:
            return False
        if col <= self.N - 3 and self.grid[row][col+1] == self.grid[row][col+2] == symbol:
            return False

        # Check for more than two identical symbols in a column
        if row >= 2 and self.grid[row-1][col] == self.grid[row-2][col] == symbol:
            return False
        if row <= self.N - 3 and self.grid[row+1][col] == self.grid[row+2][col] == symbol:
            return False

        # Check '=' and '≠' constraints
        for (r1, c1), (r2, c2) in self.equals:
            if self.grid[r1][c1] is not None and self.grid[r2][c2] is not None:
                if self.grid[r1][c1] != self.grid[r2][c2]:
                    return False

        for (r1, c1), (r2, c2) in self.notequals:
            if self.grid[r1][c1] is not None and self.grid[r2][c2] is not None:
                if self.grid[r1][c1] == self.grid[r2][c2]:
                    return False

        return True

    def backtrack(self, row=0, col=0):
        if row == self.N:
            return self.grid

        next_row, next_col = (row, col + 1) if col + 1 < self.N else (row + 1, 0)

        if self.grid[row][col] is not None:
            return self.backtrack(next_row, next_col)

        for symbol in ['S', 'M']:
            if self.is_valid(row, col, symbol):
                self.grid[row][col] = symbol
                result = self.backtrack(next_row, next_col)
                if result:
                    return result
                self.grid[row][col] = None

        return None

    def generate_clues(self):
        num_equals = random.randint(1, 5)
        num_notequals = random.randint(1, 5)

        used = set()

        while len(self.equals) < num_equals:
            r1, c1 = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            r2, c2 = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (r1, c1) != (r2, c2) and ((r1, c1), (r2, c2)) not in used:
                if self.grid[r1][c1] == self.grid[r2][c2]:
                    self.equals.append(((r1, c1), (r2, c2)))
                    used.add(((r1, c1), (r2, c2)))

        while len(self.notequals) < num_notequals:
            r1, c1 = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            r2, c2 = random.randint(0, self.N - 1), random.randint(0, self.N - 1)
            if (r1, c1) != (r2, c2) and ((r1, c1), (r2, c2)) not in used:
                if self.grid[r1][c1] != self.grid[r2][c2]:
                    self.notequals.append(((r1, c1), (r2, c2)))
                    used.add(((r1, c1), (r2, c2)))

    def mask_grid(self, num_cells_to_remove=10):
        all_cells = [(r, c) for r in range(self.N) for c in range(self.N)]
        random.shuffle(all_cells)
        for r, c in all_cells[:num_cells_to_remove]:
            self.grid[r][c] = None

    def create_grid_gui(self):
        for r in range(self.N):
            for c in range(self.N):
                btn = tk.Button(self.window, text=UNKNOWN, font=('Arial', 20), width=5, height=2,
                                command=lambda row=r, col=c: self.cell_click(row, col))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def cell_click(self, row, col):
        # Toggle between ☀️ and 🌑 on click
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'M'
        elif self.grid[row][col] == 'M':
            self.grid[row][col] = 'S'
        else:
            self.grid[row][col] = 'S'
        self.update_grid_display()

    def solve_puzzle(self):
        self.backtrack()
        self.update_grid_display()

# Helper function to start the GUI application
def start_gui():
    puzzle = TangoPuzzle(6)
    puzzle.generate_clues()
    puzzle.mask_grid(10)
    puzzle.create_grid_gui()
    puzzle.window.mainloop()

if __name__ == "__main__":
    start_gui()

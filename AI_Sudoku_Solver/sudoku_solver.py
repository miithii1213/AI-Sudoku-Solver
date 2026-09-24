import tkinter as tk
from tkinter import messagebox, ttk
import random

# =========================================================
# SUDOKU VALIDATION
# =========================================================

def is_valid(grid, row, col, num):

    # Check row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == num:
                return False

    return True


# =========================================================
# AI SUDOKU SOLVER - BACKTRACKING
# =========================================================

def solve_sudoku(grid):

    for row in range(9):
        for col in range(9):

            if grid[row][col] == 0:

                for num in range(1, 10):

                    if is_valid(grid, row, col, num):

                        grid[row][col] = num

                        if solve_sudoku(grid):
                            return True

                        grid[row][col] = 0

                return False

    return True


# =========================================================
# FAST SUDOKU GENERATOR
# =========================================================

def generate_sudoku():

    # Valid completed Sudoku pattern
    base = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],

        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],

        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
    ]

    # Randomly change the numbers
    digits = list(range(1, 10))
    random.shuffle(digits)

    grid = []

    for row in base:
        new_row = []

        for number in row:
            new_row.append(digits[number - 1])

        grid.append(new_row)

    return grid


# =========================================================
# CLEAR BOARD
# =========================================================

def clear_grid():

    for r in range(9):
        for c in range(9):

            cells[r][c].delete(0, tk.END)

            cells[r][c].config(
                foreground="#111827",
                background="white"
            )

    status_label.config(
        text="Ready for a new Sudoku puzzle",
        foreground="#475569"
    )


# =========================================================
# NEW PUZZLE
# =========================================================

def new_puzzle():

    clear_grid()

    level = difficulty.get()

    if level == "Easy":
        remove = 35
    elif level == "Medium":
        remove = 45
    else:
        remove = 55

    # Generate completed valid Sudoku
    grid = generate_sudoku()

    # Remove numbers
    positions = [
        (r, c)
        for r in range(9)
        for c in range(9)
    ]

    random.shuffle(positions)

    for r, c in positions[:remove]:
        grid[r][c] = 0

    # Display puzzle
    for r in range(9):
        for c in range(9):

            if grid[r][c] != 0:

                cells[r][c].insert(
                    0,
                    str(grid[r][c])
                )

                cells[r][c].config(
                    foreground="#111827",
                    background="#e5e7eb"
                )

    status_label.config(
        text=f"🧩 {level} puzzle ready • Click SOLVE",
        foreground="#2563eb"
    )


# =========================================================
# GET GRID
# =========================================================

def get_grid():

    grid = []

    for r in range(9):

        row = []

        for c in range(9):

            value = cells[r][c].get().strip()

            if value.isdigit():

                number = int(value)

                if 1 <= number <= 9:
                    row.append(number)
                else:
                    row.append(0)

            else:
                row.append(0)

        grid.append(row)

    return grid


# =========================================================
# CHECK DUPLICATES
# =========================================================

def check_initial_grid(grid):

    for r in range(9):
        for c in range(9):

            num = grid[r][c]

            if num != 0:

                # Temporarily remove number
                grid[r][c] = 0

                valid = is_valid(
                    grid,
                    r,
                    c,
                    num
                )

                # Restore number
                grid[r][c] = num

                if not valid:
                    return False

    return True


# =========================================================
# SOLVE BUTTON
# =========================================================

def solve_button():

    grid = get_grid()

    # Check invalid numbers
    if not check_initial_grid(grid):

        status_label.config(
            text="❌ Invalid Sudoku!",
            foreground="#dc2626"
        )

        messagebox.showerror(
            "Invalid Sudoku",
            "Duplicate number found!\n\n"
            "Please check the row, column or 3x3 box."
        )

        return

    status_label.config(
        text="🤖 AI is solving...",
        foreground="#f59e0b"
    )

    root.update_idletasks()

    # Copy grid
    solving_grid = [
        row[:]
        for row in grid
    ]

    # Solve using Backtracking
    result = solve_sudoku(solving_grid)

    if result:

        # Display solution
        for r in range(9):
            for c in range(9):

                cells[r][c].delete(
                    0,
                    tk.END
                )

                cells[r][c].insert(
                    0,
                    str(solving_grid[r][c])
                )

                cells[r][c].config(
                    foreground="#2563eb",
                    background="#eff6ff"
                )

        status_label.config(
            text="✅ Sudoku solved successfully!",
            foreground="#16a34a"
        )

        messagebox.showinfo(
            "Sudoku Solved",
            "🎉 Sudoku solved successfully!\n\n"
            "🤖 Solved using Backtracking AI."
        )

    else:

        status_label.config(
            text="❌ No solution found",
            foreground="#dc2626"
        )

        messagebox.showerror(
            "No Solution",
            "This Sudoku puzzle has no solution."
        )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title("AI Sudoku Solver")

# Small window
root.geometry("520x720")

root.resizable(False, False)

root.configure(
    background="#f8fafc"
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    background="#1e3a8a",
    height=80
)

header.pack(
    fill="x"
)


title = tk.Label(
    header,
    text="AI SUDOKU SOLVER",
    font=("Segoe UI", 20, "bold"),
    foreground="white",
    background="#1e3a8a"
)

title.pack(
    pady=(13, 2)
)


subtitle = tk.Label(
    header,
    text="Backtracking AI Sudoku Solver",
    font=("Segoe UI", 9),
    foreground="#dbeafe",
    background="#1e3a8a"
)

subtitle.pack()


# =========================================================
# DIFFICULTY
# =========================================================

control_frame = tk.Frame(
    root,
    background="#f8fafc"
)

control_frame.pack(
    pady=8
)


difficulty_label = tk.Label(
    control_frame,
    text="Difficulty:",
    font=("Segoe UI", 10, "bold"),
    foreground="#1f2937",
    background="#f8fafc"
)

difficulty_label.grid(
    row=0,
    column=0,
    padx=5
)


difficulty = tk.StringVar(
    value="Medium"
)


difficulty_box = ttk.Combobox(
    control_frame,
    textvariable=difficulty,
    values=[
        "Easy",
        "Medium",
        "Hard"
    ],
    state="readonly",
    width=10,
    font=("Segoe UI", 10)
)

difficulty_box.grid(
    row=0,
    column=1,
    padx=5
)


# =========================================================
# SUDOKU BOARD
# =========================================================

board_outer = tk.Frame(
    root,
    background="#111827",
    padx=3,
    pady=3
)

board_outer.pack(
    pady=3
)


cells = []


for r in range(9):

    row_cells = []

    for c in range(9):

        cell = tk.Entry(
            board_outer,
            width=2,
            font=("Segoe UI", 15, "bold"),
            justify="center",
            relief="flat",
            borderwidth=0,
            background="white",
            foreground="#111827"
        )

        padx_left = 1
        padx_right = 1
        pady_top = 1
        pady_bottom = 1

        # 3x3 box spacing
        if c % 3 == 0:
            padx_left = 3

        if c % 3 == 2:
            padx_right = 3

        if r % 3 == 0:
            pady_top = 3

        if r % 3 == 2:
            pady_bottom = 3

        cell.grid(
            row=r,
            column=c,
            padx=(
                padx_left,
                padx_right
            ),
            pady=(
                pady_top,
                pady_bottom
            ),
            ipadx=3,
            ipady=2
        )

        row_cells.append(cell)

    cells.append(row_cells)


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(
    root,
    background="#f8fafc"
)

button_frame.pack(
    pady=10
)


# SOLVE BUTTON

solve_button_ui = tk.Button(
    button_frame,
    text="SOLVE",
    command=solve_button,
    font=("Segoe UI", 9, "bold"),
    foreground="white",
    background="#2563eb",
    activebackground="#1d4ed8",
    relief="flat",
    width=13,
    height=2,
    cursor="hand2"
)

solve_button_ui.grid(
    row=0,
    column=0,
    padx=3
)


# NEW PUZZLE BUTTON

new_button = tk.Button(
    button_frame,
    text="NEW PUZZLE",
    command=new_puzzle,
    font=("Segoe UI", 9, "bold"),
    foreground="white",
    background="#059669",
    activebackground="#047857",
    relief="flat",
    width=13,
    height=2,
    cursor="hand2"
)

new_button.grid(
    row=0,
    column=1,
    padx=3
)


# CLEAR BUTTON

clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_grid,
    font=("Segoe UI", 9, "bold"),
    foreground="white",
    background="#dc2626",
    activebackground="#b91c1c",
    relief="flat",
    width=13,
    height=2,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=2,
    padx=3
)


# =========================================================
# STATUS
# =========================================================

status_label = tk.Label(
    root,
    text="Ready for a new Sudoku puzzle",
    font=("Segoe UI", 9),
    foreground="#475569",
    background="#f8fafc"
)

status_label.pack(
    pady=4
)


# =========================================================
# PROJECT INFO
# =========================================================

info = tk.Label(
    root,
    text="AI Technique: Backtracking • 9×9 CSP",
    font=("Segoe UI", 8),
    foreground="#64748b",
    background="#f8fafc"
)

info.pack(
    pady=2
)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()
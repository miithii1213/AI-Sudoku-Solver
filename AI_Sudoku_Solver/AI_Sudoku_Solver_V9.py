import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import time
import os
ai_step_details = []


# =========================================================
# COLORS
# =========================================================

BG = "#f1f5f9"
CARD = "#ffffff"

PRIMARY = "#2563eb"
PRIMARY_DARK = "#1d4ed8"

GREEN = "#059669"
GREEN_DARK = "#047857"

RED = "#dc2626"
RED_DARK = "#b91c1c"

TEXT = "#0f172a"
MUTED = "#64748b"

LIGHT_BLUE = "#eff6ff"
GIVEN = "#e2e8f0"
SELECTED = "#dbeafe"


# =========================================================
# GLOBAL VARIABLES
# =========================================================

solving = False
start_time = 0
solving_steps = 0
thinking_dots = 0

cells = []
selected_cell = None


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
# AI BACKTRACKING SOLVER
# =========================================================

def solve_sudoku(grid):

    global solving_steps

    for row in range(9):

        for col in range(9):

            if grid[row][col] == 0:

                for num in range(1, 10):

                    if is_valid(grid, row, col, num):

                        grid[row][col] = num

                        ai_step_details.append(
                            f"Step {len(ai_step_details) + 1} → "
                            f"Row {row + 1}, Column {col + 1} → Placed {num}"
                        )

                        solving_steps += 1

                        if solve_sudoku(grid):
                            return True

                        grid[row][col] = 0

                return False

    return True

# =========================================================
# GENERATE SUDOKU
# =========================================================

def generate_sudoku():

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
# BUTTON HOVER EFFECT
# =========================================================

def button_hover(button, normal_color, hover_color):

    def on_enter(event):
        button.config(
            background=hover_color,
            relief="raised"
        )

    def on_leave(event):
        button.config(
            background=normal_color,
            relief="flat"
        )

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


# =========================================================
# SELECTED CELL
# =========================================================

def select_cell(selected):

    global selected_cell

    # Remove border from previous cell
    if selected_cell is not None:

        try:
            selected_cell.config(
                highlightthickness=0
            )
        except:
            pass

    # Set new selected cell
    selected_cell = selected

    selected_cell.config(
        highlightbackground=PRIMARY,
        highlightcolor=PRIMARY,
        highlightthickness=2
    )


# =========================================================
# CLEAR GRID
# =========================================================

def clear_grid():

    global selected_cell

    selected_cell = None

    for r in range(9):

        for c in range(9):

            cells[r][c].delete(0, tk.END)

            cells[r][c].config(
                foreground=TEXT,
                background=CARD,
                highlightthickness=0
            )

    status_label.config(
        text="Ready • Generate a puzzle to begin",
        foreground=MUTED
    )

    steps_label.config(text="0")
    timer_label.config(text="0.00 s")


# =========================================================
# NEW PUZZLE
# =========================================================

def new_puzzle():

    global selected_cell

    selected_cell = None

    clear_grid()

    level = difficulty.get()

    if level == "Easy":
        remove = 35

    elif level == "Medium":
        remove = 45

    else:
        remove = 55

    status_label.config(
        text="Creating new puzzle...",
        foreground=PRIMARY
    )

    root.update_idletasks()

    grid = generate_sudoku()

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
                    foreground="#475569",
                    background=GIVEN
                )

    status_label.config(
        text=f"{level} puzzle ready • Press SOLVE",
        foreground=PRIMARY
    )


# =========================================================
# GET GRID FROM GUI
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
# CHECK INITIAL GRID
# =========================================================

def check_initial_grid(grid):

    for r in range(9):

        for c in range(9):

            num = grid[r][c]

            if num != 0:

                grid[r][c] = 0

                valid = is_valid(
                    grid,
                    r,
                    c,
                    num
                )

                grid[r][c] = num

                if not valid:
                    return False

    return True


# =========================================================
# TIMER
# =========================================================

def update_timer():

    if solving:

        elapsed = time.time() - start_time

        timer_label.config(
            text=f"{elapsed:.2f} s"
        )

        root.after(
            50,
            update_timer
        )


# =========================================================
# AI THINKING ANIMATION
# =========================================================

def thinking_animation():

    global thinking_dots

    if solving:

        thinking_dots = (
            thinking_dots + 1
        ) % 4

        dots = "." * thinking_dots

        status_label.config(
            text="AI is thinking" + dots,
            foreground=PRIMARY
        )

        root.after(
            400,
            thinking_animation
        )


# =========================================================
# SUCCESS SCREEN
# =========================================================

def show_success_screen(elapsed, steps):

    success = tk.Toplevel(root)

    success.title("Sudoku Solved!")

    success.geometry("380x300")

    success.resizable(
        False,
        False
    )

    success.configure(
        background=CARD
    )

    title = tk.Label(
        success,
        text="🎉 SOLVED!",
        font=("Segoe UI", 24, "bold"),
        foreground=GREEN,
        background=CARD
    )

    title.pack(
        pady=(30, 10)
    )

    message = tk.Label(
        success,
        text="Sudoku solved successfully!",
        font=("Segoe UI", 11, "bold"),
        foreground=TEXT,
        background=CARD
    )

    message.pack(
        pady=5
    )

    details = tk.Label(
        success,
        text=(
            "🤖 AI Method : Backtracking\n"
            f"⏱️ Time : {elapsed:.2f} seconds\n"
            f"🔢 Steps : {steps}"
        ),
        font=("Segoe UI", 10),
        foreground=MUTED,
        background=CARD,
        justify="center"
    )

    details.pack(
        pady=15
    )

    ok_button = tk.Button(
        success,
        text="OK",
        font=("Segoe UI", 10, "bold"),
        foreground="white",
        background=PRIMARY,
        activebackground=PRIMARY_DARK,
        relief="flat",
        width=12,
        height=2,
        command=lambda: (success.destroy(),
                         show_ai_steps()),
        cursor="hand2"
    )

    ok_button.pack(
        pady=10
    )

    button_hover(
        ok_button,
        PRIMARY,
        PRIMARY_DARK
    )

def show_ai_steps():

    steps_window = tk.Toplevel(root)

    steps_window.title("AI Solving Steps")
    steps_window.geometry("500x500")

    title = tk.Label(
        steps_window,
        text="AI Solving Steps",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=10)

    steps_text = tk.Text(
        steps_window,
        font=("Consolas", 11),
        width=55,
        height=25
    )
    steps_text.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    for step in ai_step_details:
        steps_text.insert(
            tk.END,
            step + "\n"
        )

    steps_text.config(
        state="disabled"
    )
# =========================================================
# SOLVE BUTTON
# =========================================================

def solve_button():

    global solving
    global start_time
    global solving_steps
    global thinking_dots

    # Get current puzzle
    grid = get_grid()

    # Save original puzzle
    original_grid = [
        row[:]
        for row in grid
    ]

    # Check invalid Sudoku
    if not check_initial_grid(grid):

        status_label.config(
            text="Invalid Sudoku • Check your numbers",
            foreground=RED
        )

        messagebox.showerror(
            "Invalid Sudoku",
            "Duplicate number found!\n\n"
            "Please check the row, column or 3×3 box."
        )

        return

    # Reset statistics
    solving_steps = 0
    ai_step_details.clear()
    thinking_dots = 0

    # Start solving
    solving = True

    start_time = time.time()

    status_label.config(
        text="AI is thinking...",
        foreground=PRIMARY
    )

    steps_label.config(
        text="0"
    )

    # Disable buttons while solving
    solve_button_ui.config(
        state="disabled"
    )

    new_button.config(
        state="disabled"
    )

    clear_button.config(
        state="disabled"
    )

    difficulty_box.config(
        state="disabled"
    )

    # Start animation and timer
    thinking_animation()
    update_timer()

    root.update_idletasks()

    # Create solving copy
    solving_grid = [
        row[:]
        for row in grid
    ]

    # Run AI
    result = solve_sudoku(
        solving_grid
    )

    # Stop solving
    solving = False

    elapsed = time.time() - start_time

    # Update statistics
    steps_label.config(
        text=str(solving_steps)
    )

    timer_label.config(
        text=f"{elapsed:.2f} s"
    )


    # =====================================================
    # SOLUTION FOUND
    # =====================================================

    if result:

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
                    highlightthickness=0
                )

                # Original given number
                if original_grid[r][c] != 0:

                    cells[r][c].config(
                        foreground="#475569",
                        background=GIVEN
                    )

                # AI generated number
                else:

                    cells[r][c].config(
                        foreground="#2563eb",
                        background=LIGHT_BLUE
                    )

        status_label.config(
            text="🎉 Sudoku Solved Successfully!",
            foreground=GREEN
        )

        show_success_screen(
            elapsed,
            solving_steps
        )
    

    # =====================================================
    # NO SOLUTION
    # =====================================================

    else:

        status_label.config(
            text="No solution found",
            foreground=RED
        )

        messagebox.showerror(
            "No Solution",
            "This Sudoku puzzle has no solution."
        )

    # Enable buttons again
    solve_button_ui.config(
        state="normal"
    )

    new_button.config(
        state="normal"
    )

    clear_button.config(
        state="normal"
    )

    difficulty_box.config(
        state="readonly"
    )


# =========================================================
# SPLASH SCREEN
# =========================================================

splash = tk.Tk()

splash.title(
    "AI Sudoku Solver"
)

splash.geometry(
    "420x300"
)

splash.resizable(
    False,
    False
)

splash.configure(
    background=PRIMARY
)


# =========================================================
# ICON
# =========================================================

icon_path = os.path.join(
    os.path.dirname(__file__),
    "sudoku_icon.png"
)


if os.path.exists(icon_path):

    splash_image = Image.open(
        icon_path
    )

    splash_image = splash_image.resize(
        (110, 110)
    )

    splash_photo = ImageTk.PhotoImage(
        splash_image
    )

    icon_label = tk.Label(
        splash,
        image=splash_photo,
        background=PRIMARY
    )

    icon_label.pack(
        pady=(25, 10)
    )

else:

    icon_label = tk.Label(
        splash,
        text="🧩",
        font=("Segoe UI Emoji", 65),
        foreground="white",
        background=PRIMARY
    )

    icon_label.pack(
        pady=(25, 10)
    )


# =========================================================
# SPLASH TITLE
# =========================================================

splash_title = tk.Label(
    splash,
    text="AI SUDOKU SOLVER",
    font=("Segoe UI", 22, "bold"),
    foreground="white",
    background=PRIMARY
)

splash_title.pack()


splash_subtitle = tk.Label(
    splash,
    text="Smart Sudoku Solver using Artificial Intelligence",
    font=("Segoe UI", 9),
    foreground="#dbeafe",
    background=PRIMARY
)

splash_subtitle.pack(
    pady=5
)


loading_label = tk.Label(
    splash,
    text="Starting...",
    font=("Segoe UI", 8),
    foreground="#dbeafe",
    background=PRIMARY
)

loading_label.pack(
    pady=10
)


# =========================================================
# START MAIN APPLICATION
# =========================================================

def start_main_app():

    global root
    global difficulty
    global difficulty_box
    global solve_button_ui
    global new_button
    global clear_button
    global timer_label
    global steps_label
    global status_label
    global cells

    # Close splash screen
    splash.destroy()

    # =====================================================
    # MAIN WINDOW
    # =====================================================

    root = tk.Tk()

    root.title(
        "AI Sudoku Solver"
    )

    root.geometry(
        "600x650"
    )

    root.resizable(
        False,
        False
    )

    root.configure(
        background=BG
    )


    # =====================================================
    # APP ICON
    # =====================================================

    if os.path.exists(icon_path):

        app_icon = Image.open(
            icon_path
        )

        app_icon = app_icon.resize(
            (64, 64)
        )

        app_photo = ImageTk.PhotoImage(
            app_icon
        )

        root.iconphoto(
            True,
            app_photo
        )

        root.app_photo = app_photo


    # =====================================================
    # HEADER
    # =====================================================

    header = tk.Frame(
        root,
        background=PRIMARY,
        height=100
    )

    header.pack(
        fill="x"
    )


    header_title = tk.Label(
        header,
        text="AI SUDOKU SOLVER",
        font=("Segoe UI", 22, "bold"),
        foreground="white",
        background=PRIMARY
    )

    header_title.pack(
        pady=(18, 2)
    )


    header_subtitle = tk.Label(
        header,
        text="Smart Sudoku Solver using Artificial Intelligence",
        font=("Segoe UI", 9),
        foreground="#dbeafe",
        background=PRIMARY
    )

    header_subtitle.pack()


    # =====================================================
    # CONTROL CARD
    # =====================================================

    control_card = tk.Frame(
        root,
        background=CARD,
        highlightbackground="#e2e8f0",
        highlightthickness=1
    )

    control_card.pack(
        fill="x",
        padx=20,
        pady=(14, 8)
    )


    difficulty_text = tk.Label(
        control_card,
        text="DIFFICULTY",
        font=("Segoe UI", 8, "bold"),
        foreground=MUTED,
        background=CARD
    )

    difficulty_text.grid(
        row=0,
        column=0,
        padx=(15, 5),
        pady=12
    )


    difficulty = tk.StringVar(
        value="Medium"
    )


    difficulty_box = ttk.Combobox(
        control_card,
        textvariable=difficulty,
        values=[
            "Easy",
            "Medium",
            "Hard"
        ],
        state="readonly",
        width=12,
        font=("Segoe UI", 10)
    )

    difficulty_box.grid(
        row=0,
        column=1,
        padx=5
    )


    # =====================================================
    # BOARD TITLE
    # =====================================================

    board_title = tk.Label(
        root,
        text="PUZZLE BOARD",
        font=("Segoe UI", 9, "bold"),
        foreground=MUTED,
        background=BG
    )

    board_title.pack(
        pady=(4, 5)
    )


   # =====================================================
    # SUDOKU BOARD
    # =====================================================

    board_outer = tk.Frame(
        root,
        background=TEXT,
        padx=4,
        pady=4
    )

    board_outer.pack(
        pady=2
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
                background=CARD,
                foreground=TEXT,
                selectbackground=SELECTED,
                selectforeground=TEXT,
                highlightthickness=0
            )


            # Normal spacing
            padx_left = 1
            padx_right = 1
            pady_top = 1
            pady_bottom = 1


            # 3x3 box borders
            if c % 3 == 0:
                padx_left = 4

            if c % 3 == 2:
                padx_right = 4

            if r % 3 == 0:
                pady_top = 4

            if r % 3 == 2:
                pady_bottom = 4


            cell.grid(
                row=r,
                column=c,
                padx=(padx_left, padx_right),
                pady=(pady_top, pady_bottom),
                ipadx=3,
                ipady=2
            )


            # Cell selection
            cell.bind(
                "<Button-1>",
                lambda event, current_cell=cell:
                select_cell(current_cell)
            )


            row_cells.append(
                cell
            )

        cells.append(
            row_cells
        )


    # =====================================================
    # BUTTON FRAME
    # =====================================================

    button_frame = tk.Frame(
        root,
        background=BG
    )

    button_frame.pack(
        pady=12
    )


    # =====================================================
    # SOLVE BUTTON
    # =====================================================

    solve_button_ui = tk.Button(
        button_frame,
        text="SOLVE",
        command=solve_button,
        font=("Segoe UI", 9, "bold"),
        foreground="white",
        background=PRIMARY,
        activebackground=PRIMARY_DARK,
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )

    solve_button_ui.grid(
        row=0,
        column=0,
        padx=4
    )

    button_hover(
        solve_button_ui,
        PRIMARY,
        PRIMARY_DARK
    )


    # =====================================================
    # NEW PUZZLE BUTTON
    # =====================================================

    new_button = tk.Button(
        button_frame,
        text="NEW PUZZLE",
        command=new_puzzle,
        font=("Segoe UI", 9, "bold"),
        foreground="white",
        background=GREEN,
        activebackground=GREEN_DARK,
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )

    new_button.grid(
        row=0,
        column=1,
        padx=4
    )

    button_hover(
        new_button,
        GREEN,
        GREEN_DARK
    )


    # =====================================================
    # CLEAR BUTTON
    # =====================================================

    clear_button = tk.Button(
        button_frame,
        text="CLEAR",
        command=clear_grid,
        font=("Segoe UI", 9, "bold"),
        foreground="white",
        background=RED,
        activebackground=RED_DARK,
        relief="flat",
        width=12,
        height=2,
        cursor="hand2"
    )

    clear_button.grid(
        row=0,
        column=2,
        padx=4
    )

    button_hover(
        clear_button,
        RED,
        RED_DARK
    )


    # =====================================================
    # STATISTICS CARD
    # =====================================================

    stats_card = tk.Frame(
        root,
        background=CARD,
        highlightbackground="#e2e8f0",
        highlightthickness=1
    )

    stats_card.pack(
        fill="x",
        padx=20,
        pady=(2, 8)
    )


    # TIME
    time_title = tk.Label(
        stats_card,
        text="TIME",
        font=("Segoe UI", 8, "bold"),
        foreground=MUTED,
        background=CARD
    )

    time_title.grid(
        row=0,
        column=0,
        padx=45,
        pady=(8, 0)
    )


    timer_label = tk.Label(
        stats_card,
        text="0.00 s",
        font=("Segoe UI", 12, "bold"),
        foreground=PRIMARY,
        background=CARD
    )

    timer_label.grid(
        row=1,
        column=0,
        padx=45,
        pady=(0, 8)
    )


    # STEPS
    steps_title = tk.Label(
        stats_card,
        text="STEPS",
        font=("Segoe UI", 8, "bold"),
        foreground=MUTED,
        background=CARD
    )

    steps_title.grid(
        row=0,
        column=1,
        padx=45,
        pady=(8, 0)
    )


    steps_label = tk.Label(
        stats_card,
        text="0",
        font=("Segoe UI", 12, "bold"),
        foreground=GREEN,
        background=CARD
    )

    steps_label.grid(
        row=1,
        column=1,
        padx=45,
        pady=(0, 8)
    )


    # =====================================================
    # STATUS
    # =====================================================

    status_label = tk.Label(
        root,
        text="Ready • Generate a puzzle to begin",
        font=("Segoe UI", 9, "bold"),
        foreground=MUTED,
        background=BG
    )

    status_label.pack(
        pady=(3, 5)
    )


    # =====================================================
    # INFO
    # =====================================================

    info_label = tk.Label(
        root,
        text="AI Method: Backtracking  •  Problem Type: 9×9 CSP",
        font=("Segoe UI", 8),
        foreground=MUTED,
        background=BG
    )

    info_label.pack()


    # =====================================================
    # VERSION
    # =====================================================

    version_label = tk.Label(
        root,
        text="AI Sudoku Solver • Version 8.0",
        font=("Segoe UI", 7),
        foreground="#94a3b8",
        background=BG
    )

    version_label.pack(
        pady=(4, 0)
    )


    # =====================================================
    # START MAIN LOOP
    # =====================================================

    root.mainloop()


# =========================================================
# START SPLASH
# =========================================================

splash.after(
    4000,
    start_main_app
)

splash.mainloop()
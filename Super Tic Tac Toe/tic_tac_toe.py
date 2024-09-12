from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Super Tic Tac Toe')

# Global variables
clicked = True
count = 0
subgrid_wins = [[None for _ in range(3)] for _ in range(3)]  # Track who wins each subgrid
current_subgrid = None  # Which subgrid the player is allowed to play in next
player_colors = {"X": "#FF6F61", "O": "#6BAED6"}  # Player color scheme

# To disable all buttons in a subgrid
def disableSubgridButtons(grid):
    for row in grid:
        for btn in row:
            btn.config(state=DISABLED)

# Check if a player has won a 3x3 subgrid
def checkSubgridWinner(subgrid):
    for row in range(3):
        if subgrid[row][0]["text"] == subgrid[row][1]["text"] == subgrid[row][2]["text"] != " ":
            return subgrid[row][0]["text"]
    for col in range(3):
        if subgrid[0][col]["text"] == subgrid[1][col]["text"] == subgrid[2][col]["text"] != " ":
            return subgrid[0][col]["text"]
    if subgrid[0][0]["text"] == subgrid[1][1]["text"] == subgrid[2][2]["text"] != " ":
        return subgrid[0][0]["text"]
    if subgrid[0][2]["text"] == subgrid[1][1]["text"] == subgrid[2][0]["text"] != " ":
        return subgrid[0][2]["text"]
    return None

# Check if someone won the overall game by winning subgrids
def checkOverallWinner():
    global subgrid_wins
    for row in range(3):
        if subgrid_wins[row][0] == subgrid_wins[row][1] == subgrid_wins[row][2] and subgrid_wins[row][0] is not None:
            return subgrid_wins[row][0]
    for col in range(3):
        if subgrid_wins[0][col] == subgrid_wins[1][col] == subgrid_wins[2][col] and subgrid_wins[0][col] is not None:
            return subgrid_wins[0][col]
    if subgrid_wins[0][0] == subgrid_wins[1][1] == subgrid_wins[2][2] and subgrid_wins[0][0] is not None:
        return subgrid_wins[0][0]
    if subgrid_wins[0][2] == subgrid_wins[1][1] == subgrid_wins[2][0] and subgrid_wins[0][2] is not None:
        return subgrid_wins[0][2]
    return None

# Update player label to show the current player
def updatePlayerLabel():
    player_label.config(text=f"Player {'X' if clicked else 'O'}'s turn", fg=player_colors["X"] if clicked else player_colors["O"])

# Button click logic
def buttonClicked(button, row, col, subgrid_row, subgrid_col):
    global clicked, count, current_subgrid
    
    # Enforce subgrid restriction if it's not the first move
    if current_subgrid and (current_subgrid != (row, col)):
        messagebox.showerror("Super Tic Tac Toe", "Please play in the correct subgrid!")
        return

    if button["text"] == " ":
        button["text"] = "X" if clicked else "O"
        button.config(fg=player_colors[button["text"]], bg="#f0f0f0")
        clicked = not clicked
        count += 1
        
        # Check if this subgrid has a winner
        winner = checkSubgridWinner(subgrids[row][col])
        if winner:
            subgrid_wins[row][col] = winner
            disableSubgridButtons(subgrids[row][col])
            overall_winner = checkOverallWinner()
            if overall_winner:
                messagebox.showinfo("Super Tic Tac Toe", f"Player {overall_winner} wins the game!")
                start()
                return

        # Check for draw (when all subgrids are filled)
        if all(all(cell["text"] != " " for row in subgrid for cell in row) for subgrid in subgrids):
            messagebox.showerror("Super Tic Tac Toe", "Draw, play again!")
            start()
            return

        # Set the next subgrid based on the last move
        current_subgrid = (subgrid_row, subgrid_col)
        updatePlayerLabel()  # Update the turn display
    else:
        messagebox.showerror("Super Tic Tac Toe", "Please select another box.")

# Start a new game
def start():
    global subgrids, clicked, count, current_subgrid, subgrid_wins
    clicked = True
    count = 0
    current_subgrid = None
    subgrid_wins = [[None for _ in range(3)] for _ in range(3)]

    # Create the 9x9 grid (9 subgrids, each a 3x3 grid inside a container Frame)
    subgrids = [[None for _ in range(3)] for _ in range(3)]
    
    for row in range(3):
        for col in range(3):
            # Create a frame container for each 3x3 subgrid
            subgrid_frame = Frame(root, bd=5, relief="ridge")
            subgrid_frame.grid(row=row, column=col, padx=5, pady=5)
            subgrids[row][col] = [[Button(subgrid_frame, text=" ", font=("Helvetica", 12, "bold"), height=2, width=5, relief="solid", bd=2,
                                          command=lambda r=row, c=col, sr=i, sc=j: buttonClicked(subgrids[r][c][sr][sc], r, c, sr, sc)) 
                                  for j in range(3)] for i in range(3)]
            for i in range(3):
                for j in range(3):
                    subgrids[row][col][i][j].grid(row=i, column=j, padx=1, pady=1)


# Create game menu
gameMenu = Menu(root)
root.config(menu=gameMenu)

# Create game options menu
optionMenu = Menu(gameMenu, tearoff=False)
gameMenu.add_cascade(label="Options", menu=optionMenu)
optionMenu.add_command(label="Restart Game", command=start)

# Start the game
start()
root.mainloop()
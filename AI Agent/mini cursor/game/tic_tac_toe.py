import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe")

        self.current_player = "X"
        self.board = ["" for _ in range(9)]
        self.buttons = []

        for i in range(3):
            for j in range(3):
                button = tk.Button(master,
                                   text="",
                                   font=("Arial", 60),
                                   width=3,
                                   height=1,
                                   command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")
                self.buttons.append(button)

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def button_click(self, row, col):
        index = row * 3 + col
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != "":
                return True
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != "":
                return True
        if self.board[0] == self.board[4] == self.board[8] != "":
            return True
        if self.board[2] == self.board[4] == self.board[6] != "":
            return True
        return False

    def check_draw(self):
        return all(cell != "" for cell in self.board)

    def reset_board(self):
        self.board = ["" for _ in range(9)]
        for button in self.buttons:
            button.config(text="")
        self.current_player = "X"

root = tk.Tk()
tt = TicTacToe(root)
root.mainloop()
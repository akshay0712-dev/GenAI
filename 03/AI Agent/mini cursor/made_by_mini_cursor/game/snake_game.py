import tkinter as tk
import random

class SnakeGame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid()
        self.board_size = 400
        self.cell_size = 20
        self.board_width = self.board_size // self.cell_size
        self.board_height = self.board_size // self.cell_size
        self.snake = [(5, self.board_height // 2), (4, self.board_height // 2), (3, self.board_height // 2)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.score = 0
        self.delay = 100

        self.canvas = tk.Canvas(self, bg='black', width=self.board_size, height=self.board_size)
        self.canvas.pack()

        self.score_label = tk.Label(self, text='Score: 0', font=('Arial', 12))
        self.score_label.pack()

        self.bind_all('<Key>', self.change_direction)

        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, self.board_width - 1)
            y = random.randint(0, self.board_height - 1)
            if (x, y) not in self.snake:
                return x, y

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Right':
            new_head = (head_x + 1, head_y)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)

        if (new_head[0] < 0 or new_head[0] >= self.board_width or
            new_head[1] < 0 or new_head[1] >= self.board_height or
            new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f'Score: {self.score}')
            self.food = self.create_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete(tk.ALL)

        self.canvas.create_rectangle(self.food[0] * self.cell_size, self.food[1] * self.cell_size,
                                     (self.food[0] + 1) * self.cell_size, (self.food[1] + 1) * self.cell_size,
                                     fill='red')

        for x, y in self.snake:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                         fill='green')

    def change_direction(self, event):
        if event.keysym == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction = 'Down'
        elif event.keysym == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.direction = 'Right'

    def update(self):
        self.move_snake()
        self.draw()
        self.after(self.delay, self.update)

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.board_size / 2, self.board_size / 2,
                                 fill='white', font='Arial 20 bold', text='Game Over! Score: {}'.format(self.score))

root = tk.Tk()
root.title('Snake Game')
game = SnakeGame(master=root)
game.mainloop()
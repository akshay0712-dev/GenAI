import tkinter as tk
import math

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Calculator")
        master.configure(bg='#f0d8a7')  # Beige background

        self.display = tk.Entry(master, width=25, borderwidth=5, font=('Arial', 20), justify='right', bg='#e8c07d', fg='#333333')  # Brownish display
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipady=20)

        # Define buttons
        self.basic_buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'pow',
            '1', '2', '3', '-', '%',
            '0', '.', '=', '+', '(', ')',
            'C', '<-'  # Clear and Backspace button
        ]

        self.scientific_buttons = ['sin', 'cos', 'tan', 'log', 'exp']

        self.button_objects = []
        button_width = 6 # Set fix width
        button_height = 2 # set fix height
        self.scientific_mode = False
        self.history_mode = False # Initialize history_mode here

        # Create buttons
        self.create_buttons()

        # Configure row and column weights for resizing
        for i in range(7): #increased range for scientific toggle
            master.grid_rowconfigure(i, weight=1)
        for i in range(5):
            master.grid_columnconfigure(i, weight=1)

        # History Log
        self.history = []
        self.history_listbox = tk.Listbox(master, width=40, height=10, font=('Arial', 12), bg='#e0ac69', fg='#333333', borderwidth=2, relief='sunken')  # Styling the listbox

        #History Button
        self.history_button = tk.Button(master, text="History",width = button_width, height = button_height, font=('Arial', 14), command=self.toggle_history, bg='#c68642', fg='white', activebackground='#a86a2a', relief='raised', borderwidth=2)
        self.history_button.grid(row=7, column=4, padx=5, pady=5, sticky='nsew')

        # Scientific Mode Toggle
        self.scientific_toggle_button = tk.Button(master, text="Scientific Mode", width=button_width, height=button_height, font=('Arial', 14), command=self.toggle_scientific_mode, bg='#c68642', fg='white', activebackground='#a86a2a', relief='raised', borderwidth=2)
        self.scientific_toggle_button.grid(row=7, column=3, padx=5, pady=5, sticky='nsew')

        self.expression = ""

    def create_buttons(self):
        # Clear existing buttons
        for button in self.button_objects:
            button.grid_forget()
        self.button_objects = []

        row_val = 1
        col_val = 0
        buttons = self.basic_buttons + (self.scientific_buttons if self.scientific_mode else [])

        for button_text in buttons:
            if button_text == 'C':
                button = tk.Button(self.master, text=button_text, width = 6, height = 2, font=('Arial', 14), command=self.clear, bg='#c68642', fg='white', activebackground='#a86a2a', relief='raised', borderwidth=2)
            elif button_text == '<-':
                button = tk.Button(self.master,text=button_text, width = 6, height = 2, font=('Arial', 14), command=self.backspace, bg='#c68642', fg='white', activebackground='#a86a2a', relief='raised', borderwidth=2)
            elif button_text == '=':
                button = tk.Button(self.master,text=button_text, width = 6, height = 2, font=('Arial', 14), command=self.calculate, bg='#c68642', fg='white', activebackground='#a86a2a', relief='raised', borderwidth=2)
            elif button_text in self.scientific_buttons:
                 button = tk.Button(self.master,text=button_text, width = 6, height = 2, font=('Arial', 14), command=lambda text=button_text: self.scientific_operation(text), bg='#b8860b', fg='white', activebackground='#966f33', relief='raised', borderwidth=2)
            else:
                button = tk.Button(self.master,text=button_text, width = 6, height = 2, font=('Arial', 14), command=lambda text=button_text: self.button_click(text), bg='#b8860b', fg='white', activebackground='#966f33', relief='raised', borderwidth=2)

            button.grid(row=row_val, column=col_val, padx=5, pady=5, sticky='nsew')
            self.button_objects.append(button)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

    def button_click(self, text):
        self.expression = self.expression + str(text)
        self.display.insert(tk.END, text)

    def clear(self):
        self.display.delete(0, tk.END)
        self.expression = ""

    def backspace(self):
        current_text = self.display.get()
        self.display.delete(len(current_text)-1, tk.END)
        self.expression = current_text[:-1]

    def calculate(self):
        try:
            # Replace 'sqrt' and 'pow' for evaluation
            expression = self.expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('pow', '**')
            expression = expression.replace('%', '/100') # percentage implementation
            result = eval(expression)

            # Update History
            full_expression = self.display.get()
            self.history.append(f'{full_expression} = {result}')

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.expression = str(result)
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expression = ""

    def toggle_history(self):
        self.history_mode = not self.history_mode
        if self.history_mode:
            # Hide buttons
            for button in self.button_objects:
                button.grid_remove()
            self.display.grid_remove()
            self.history_button.config(text="Calculator")
            self.history_listbox.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')
            self.update_history_listbox()
        else:
            # Show buttons
            self.create_buttons()
            self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipady=10)
            self.history_button.config(text="History")
            self.history_listbox.grid_remove()

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        self.create_buttons()

    def scientific_operation(self, operation):
         try:
            current_value = float(self.display.get())
            if operation == 'sin':
                result = math.sin(math.radians(current_value))
            elif operation == 'cos':
                result = math.cos(math.radians(current_value))
            elif operation == 'tan':
                result = math.tan(math.radians(current_value))
            elif operation == 'log':
                result = math.log10(current_value) if current_value > 0 else "Error"
            elif operation == 'exp':
                result = math.exp(current_value)
            else:
                result = "Error"

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.expression = str(result)
         except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expression = ""

root = tk.Tk()
root.configure(bg='#f0d8a7')  # Beige background
calc = Calculator(root)
root.mainloop()
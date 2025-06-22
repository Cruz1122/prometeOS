import tkinter as tk
from math import sin, cos, tan, sqrt, radians
import argparse
import sys
import os

# Add the project root directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="User directory", type=str)
parser.add_argument("privilege", help="User privilege level", type=str)

args = parser.parse_args()

user_directory = args.user_directory


class Calculator:
    """
    Scientific calculator application class
    """
    
    def __init__(self, root):
        """
        Initialize the calculator application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.iconbitmap(util.get_app_icon_path("calculadora", "icon.ico"))
        self.root.title("Scientific Calculator")
        self.root.config(bg="#302939")
        self.expression = ""
        self.input_text = tk.StringVar()
        
        # Center the window
        window_width = 1100
        window_height = 600

        position_top = int(
            self.root.winfo_screenheight() / 2 - self.root.winfo_screenheight() / 2
        )
        position_right = int(
            self.root.winfo_screenwidth() / 2 - self.root.winfo_screenwidth() / 2
        )
        self.root.geometry(
            f"{window_width}x{window_height}+{position_right}+{position_top}"
        )

        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        """Create and configure the calculator widgets"""
        input_frame = tk.Frame(self.root, bd=0, relief=tk.RIDGE, bg="#302939")
        input_frame.pack(side=tk.TOP)

        input_field = tk.Entry(input_frame, font=('microsoftphagspa', 28, 'bold'), textvariable=self.input_text, width=50, bg="#302939", fg="white", bd=0, justify=tk.RIGHT)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=30)  # increase the height of the input box

        btns_frame = tk.Frame(self.root, bg="#302939")
        btns_frame.pack()

        # Calculator buttons
        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', 'sqrt',
            '1', '2', '3', '-', 'sin',
            '0', '.', '=', '+', 'cos',
            '(', ')', 'tan'
        ]

        row = 0
        col = 0
        for button in buttons:
            if button not in {'sin', 'cos', 'tan', 'sqrt'}:
                if button == '=':
                    tk.Button(btns_frame, text=button, fg="black", width=30, height=6, bd=0, bg="#e99b9b", cursor="hand2",
                              command=lambda x=button: self.btn_click(x)).grid(row=row, column=col, padx=1, pady=1)
                else:
                    tk.Button(btns_frame, text=button, fg="white", width=30, height=6, bd=0, bg="#493e57", cursor="hand2",
                          command=lambda x=button: self.btn_click(x)).grid(row=row, column=col, padx=1, pady=1)
            else:
                tk.Button(btns_frame, text=button, fg="black", width=30, height=6, bd=0, bg="#e07171", cursor="hand2",
                          command=lambda x=button: self.scientific_function(x)).grid(row=row, column=col, padx=1, pady=1)

            col += 1
            if col > 4:
                col = 0
                row += 1

    def btn_click(self, item):
        """
        Handle button clicks for basic operations
        
        Args:
            item (str): Button text/value
        """
        if item == 'C':
            self.expression = ""
            self.input_text.set("")
        elif item == '=':
            try:
                result = str(eval(self.expression))
                self.input_text.set(result)
                self.expression = result
            except Exception as e:
                self.input_text.set("Error")
                self.expression = ""
        else:
            self.expression += str(item)
            self.input_text.set(self.expression)

    def scientific_function(self, func):
        """
        Handle scientific function calculations
        
        Args:
            func (str): Function name (sin, cos, tan, sqrt)
        """
        try:
            value = eval(self.expression)
            if func == 'sin':
                result = sin(radians(value))
            elif func == 'cos':
                result = cos(radians(value))
            elif func == 'tan':
                result = tan(radians(value))
            elif func == 'sqrt':
                result = sqrt(value)
            self.input_text.set(str(result))
            self.expression = str(result)
        except Exception as e:
            self.input_text.set("Error")
            self.expression = ""


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()

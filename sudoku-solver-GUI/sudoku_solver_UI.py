## Main UI

from tkinter import *
from tkinter import messagebox
import tkinter as tk
import numpy as np
import sudoku_solver_func as sudsolver
import webbrowser
from copy import copy, deepcopy

class MainWindow(Frame):

    def __init__(self, master):
        Frame.__init__(self)
        
        self.master = master
        self.master.minsize(540,640)
        self.master.maxsize(540,640)

        # Center window on user's screen
        self.center_window(540,640)

        # Catch if user clicks upper corner 'x' using built-in tkinter method
        self.master.protocol("WM_DELETE_WINDOW", self.exit)
        
        # Instantiate the Tkinter menu dropdown object 
        # This is the menu that will appear at the top of our window
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        helpmenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", accelerator="Ctrl+Q", command = self.exit)
        helpmenu.add_command(label="How to use this program", accelerator="Ctrl+H", command = self.helpbox)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=menubar)
        
        self.master.title("Sudoku Solver")
        self.titlelabel = Label(self.master, text="Sudoku Solver", font=("Helvetica", "16"))
        self.titlelabel.grid(row=0, column=0, columnspan=4, sticky="ew")
        
        # The canvas for the game board
        self.canvas = Canvas(master, width=490, height=490)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.row, self.col = -1,-1

        # draw game board on canvas
        self.__draw_grid()
        # create blank board object
        self.board_obj = np.zeros((9,9), dtype=int)

        # set behavior within game board space
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)
        
        # Reveal Solution Button
        self.reveal_button = Button(self.master, text="Reveal Solution", font=("Helvetica", "12"), relief=RAISED, fg="green",
                                    bg="lightblue", command=self.reveal_solution)
        self.reveal_button.grid(row=4, column=0, padx=25, pady=5, sticky="ew")
        
        # Clear Board Button
        self.clearbut = Button(self.master, text="Clear Board", font=("Helvetica", "12"), relief=RAISED, command=self.clear_board,
                              fg="red", bg="lightblue")
        self.clearbut.grid(row=4, column=1, padx=25, pady=5, sticky="ew")
        
        self.mylink = Label(self.master, text="Created by Andy Schultheiss", borderwidth=3, fg="blue", cursor="hand2")
        self.mylink.grid(row=5, columnspan=5, sticky="ew")
        self.mylink.bind("<Button-1>", lambda e: self.callback("https://www.andyeschultheiss.com"))


    def center_window(self, w, h):
        # get user's screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # calculate x and y coordinates to paint app centered on the user's screen
        x = int((screen_width/2) - (w/2))
        y = int((screen_height/2) - (h/2))
        centerGeo = self.master.geometry('{}x{}+{}+{}'.format(w, h, x, y))
        return centerGeo

    # function to open link in web browser
    def callback(self, url):
        webbrowser.open_new(url)

    # Exit function
    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.master.destroy()
        else:
            pass

    def helpbox(self):
        messagebox.showinfo("Help", "Click on a cell to select it. \nEnter \".\" to clear a cell or a number (1-9) to fill it. \nNavigate using the arrow keys.")


    '''A function to open a link in a web browser'''
    def callback(self, url):
        webbrowser.open_new(url)


    '''Draw grid divided with blue lines into 3x3 squares'''
    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = 20 + i * 50
            y0 = 20
            x1 = 20 + i * 50
            y1 = 490 - 20
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = 20
            y0 = 20 + i * 50
            x1 = 490 - 20
            y1 = 20 + i * 50
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    '''Draws the puzzle on the grid after erasing the previous entries'''
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.board_obj[i][j]
                if answer != 0:
                    x = 20 + j * 50 + 50 / 2
                    y = 20 + i * 50 + 50 / 2
                    self.canvas.create_text(x, y, text=answer, font=("Helvetica", "12"), tags="numbers", fill="black")
                    
    '''Draws the puzzle solution. This function is called when the user clicks on the reveal solution button'''
    def draw_soln_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.solution_board[i][j]
                x = 20 + j * 50 + 50 / 2
                y = 20 + i * 50 + 50 / 2
                original = self.board_obj[i][j]
                if answer == original:
                    textcolor = "black"
                else:
                    textcolor = "teal"
                self.canvas.create_text(x, y, text=answer, font=("Helvetica", "12"), tags="numbers", fill=textcolor)
    
    '''Highlight selected square'''                
    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = 20 + self.col * 50 + 1
            y0 = 20 + self.row * 50 + 1
            x1 = 20 + (self.col + 1) * 50 - 1
            y1 = 20 + (self.row + 1) * 50 - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    '''Handle mouse clicks by determining the cell in which the user clicked.'''
    def __cell_clicked(self, event):
        x, y = event.x, event.y
        if 20 < x < 470 and 20 < y < 470:
            self.canvas.focus_set()
            row, col = (y - 20) // 50, (x - 20) // 50
            # if cell was selected already, deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    '''Handle key presses'''
    def __key_pressed(self, event):
        
        # Right arrow
        if self.row >= 0 and self.col >=0 and self.row <= 8 and self.col <= 7 and event.keysym == "Right":
            self.col = self.col + 1
            self.__draw_cursor()
            
        # Left arrow
        if self.row >= 0 and self.col >=1 and self.row <= 8 and self.col <= 8 and event.keysym == "Left":
            self.col = self.col - 1
            self.__draw_cursor()
            
        #  Up arrow
        if self.row >= 1 and self.col >=0 and self.row <= 8 and self.col <= 8 and event.keysym == "Up":
            self.row = self.row - 1
            self.__draw_cursor()
            
        # Down arrow
        if self.row >= 0 and self.col >=0 and self.row <= 7 and self.col <= 8 and event.keysym == "Down":
            self.row = self.row + 1
            self.__draw_cursor()

        # Only numerical entries accepted
        if self.row >= 0 and self.col >= 0 and event.char in ['1','2','3','4','5','6','7','8','9']:
            self.board_obj[self.row][self.col] = int(event.char)
            self.__draw_puzzle()
            
        if self.row >= 0 and self.col >= 0 and event.char == ".":
            self.board_obj[self.row][self.col] = 0
            self.__draw_puzzle()
            
    '''The command function for the reveal function button. This function redraws
     the solution grid and disables the reveal solution button'''
    def reveal_solution(self):
        # store original board to compare, use deepcopy
        self.solution_board = deepcopy(self.board_obj)
        
        if not sudsolver.checkvalidpuzzle(self, self.solution_board):
            messagebox.showerror("Invalid Puzzle", "The puzzle board is invalid, please correct entries and try again")
            return
        if not sudsolver.solve(self.solution_board):
            messagebox.showerror("No Solution", "This puzzle has no solution")
            return
        else:
            sudsolver.solve(self.solution_board)
            self.draw_soln_puzzle()
            messagebox.showinfo("Solution Revealed", "Success! Solution found.")
            self.reveal_button.configure(bg="lightgray", fg="gray", state=DISABLED)

    def clear_board(self):
        if messagebox.askyesno("Clear Board", "Are you sure you want to clear the game board?"):
            self.board_obj = np.zeros((9,9), dtype=int)
            self.__draw_puzzle()
            self.reveal_button.configure(bg="lightblue", fg="green", state=NORMAL)
        else:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    App = MainWindow(root)
    root.mainloop()
    

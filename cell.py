from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    # Public class attribute
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self, x,y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.cell_btn_obj = None
        self.is_mine_candidate = False
        self.x = x
        self.y = y

        '''
        Append the object to the Cell.all list to have access 
        to all the instances in one place
        '''
        Cell.all.append(self)  # Access a class attribute by prepending the class name along with the attribute name
    def create_btn_obj(self, location):
        btn = Button(
            location,
            width=12,
            height=4
        )

        # Assign an event to button
        btn.bind('<Button-1>', self.left_click_actions) #left
        btn.bind('<Button-2>', self.right_click_actions) #right

        self.cell_btn_obj = btn

    @staticmethod # Static methods are used for the class on not for every instance of the class
    def create_cell_count_label(location):
        lbl = Label(
            location,
            width=12,
            height=4,
            bg='black',
            fg='white',
            font=("", 30),
            text=f"Cells Left: {Cell.cell_count}"
        )

        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        print(self.is_mine)
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You Won the Game!', 'Game Over', 0)

            # Cancel Left and Right click events if a cell is already opened:
            self.cell_btn_obj.unbind('<Button-1>')
            self.cell_btn_obj.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property # Converts this method into an attribute
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None] # list comprehension that removes all the None values
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def show_mine(self):
        self.cell_btn_obj.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_obj.configure(text=self.surrounded_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                text=f"Cells Left: {Cell.cell_count}"
                )

                self.cell_btn_obj.configure(highlightbackground="SystemButtonFace")
        self.is_opened = True

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_obj.configure(bg='orange', text="Candidate")
            self.is_mine_candidate = True
        else:
            self.cell_btn_obj.configure(highlightbackground='SystemButtonFace', text='')
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all,  settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell ({self.x}, {self.y})"
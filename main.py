from tkinter import *
from cell import Cell
import settings
import utils

root = Tk()

# Additional configuration to window
root.configure(bg='black')

# Change size of window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')

# Change title of window
root.title('Minesweeper')

# Set fixed size of window
root.resizable(False, False)

# Create a frame to contain additional elements within window

'''
TOP FRAME
'''
top_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_prct(25)
)

top_frame.place( x=0, y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper Game',
    font=('', 48)
)

game_title.place(
    x=utils.width_prct(25),
    y=0
)

'''
LEFT FRAME
'''
left_frame = Frame(
    root,
    bg='black',
    width=utils.width_prct(25),
    height=utils.height_prct(75)
)
left_frame.place(x=0, y=utils.height_prct(25))

'''
CENTER FRAME
'''
center_frame = Frame(
    root,
    bg='black',
    width=utils.width_prct(75),
    height=utils.height_prct(75)
)

center_frame.place(x=utils.width_prct(25), y= utils.height_prct(25))

'''
CREATE CELLS
'''
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE ):
        c = Cell(x,y)
        c.create_btn_obj(center_frame)
        c.cell_btn_obj.grid(column=x, row=y)

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)

Cell.randomize_mines()

# Runs the window
root.mainloop()
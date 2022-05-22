from ctypes import util
from tkinter import *
import mysettings
import utilities
from cell import Cell


root = Tk()          # This is just a regular window.
 # Label(), Frame() are functions in tkinter

    # SETTINGS OF THE WINDOW 
root.configure(bg='cyan')   # to change background color of the window

root.geometry(f'{mysettings.WIDTH}x{mysettings.HEIGHT}')
root.title('Minesweeper-Can you win?')
root.resizable(False, False)   # To avoid resizing (maximizing). 2 Falses for ht and width

# ---------------
       # DIVIDING THE WINDOW INTO FRAMES

  # FRAME 1 : Let's create a frame which is top part of the window
top_frame = Frame(      # Instantiate the class Frame
    root,
    bg = 'yellow',  # to differentiate the color of this frame from the background window.
    width= mysettings.WIDTH,
    height=utilities.ht_in_percent(20)
)     
top_frame.place(x=0, y=0)  # Specify the location to place it in the window in relational aspect.

game_title = Label(
  top_frame,
  bg='yellow',
  fg ='red',
  text = 'Minesweeper - Can you win ??',
  font=('', 48)
)
game_title.place(
  x = utilities.width_percent(25), y =utilities.ht_in_percent(5)
)

 # FRAME 2 : to show the current statistics
left_frame = Frame(
    root,
    bg = 'black',
    width=utilities.width_percent(20),   # 1/5th
    height=utilities.ht_in_percent(80)
)
left_frame.place(x=0, y= utilities.ht_in_percent(20))

 # FRAME 3 : Frame containing the cells of the actual game
center_frame = Frame(
    root,
    bg = 'green',
    width = utilities.width_percent(80),
    height=utilities.ht_in_percent(80)
)
center_frame.place(x = utilities.width_percent(20), y = utilities.ht_in_percent(20))

# --------------

  # BUILDING THE GRID OF CELLS FOR THE GAME

for x in range(mysettings.GRID_SIZE):
  for y in range(mysettings.GRID_SIZE):
    c = Cell(x,y)
    c.create_btn(center_frame)
    c.cell_btn.grid(column = x,    # position the new button at different positions in grid
    row = y)


     # SHOW GAME'S LIVE STATISTICS
# Call the label function from cell class
Cell.create_cell_count_label(left_frame)
Cell.total_cell_count_label.place(
  x=0, y = 0
)

      # PUT MINES IN RANDOM CELLS
Cell.randomize_mines()

        # DISABLE ALL THE BUTTONS AFTER THE GAME IS OVER
if Cell.game_over_flag : 
  for w in center_frame.winfo_children():
          w.configure(state="disabled")


   # RUN THE WINDOW
root.mainloop()       # To close a window that we opened 
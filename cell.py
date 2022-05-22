import mimetypes
from tkinter import Button, Label
import random
import mysettings
import sys

class Cell:
       # STATIC VARIABLES FOR ALL CELLS TOGETHER

    all = [] # to contain info about all instances
    cell_count = mysettings.CELL_COUNT
    total_cell_count_label = None
    game_over_flag = 0


            # INITIATE INDIVIDUAL CELL
    def __init__(self,x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False   # Whether user put a flag on it or not.
        self.cell_btn = None
        self.x = x
        self.y = y

        # append the object info to the Cell.all list
        Cell.all.append(self)


       # TO CREATE A BUTTON FOR EACH CELL
    def create_btn(self, location):
        btn = Button(
            location,
            width=3,
            height=2,
        )

        # bind() function lets us specify what should happen when a button is clicked.
        # <Button-1> - is for left click and , <Button-2> is for right click (for Mac)
        btn.bind('<Button-1>', self.left_click_action )
        btn.bind('<Button-2>', self.right_click_action)
        self.cell_btn = btn


         # SPECIFY WHAT HAPPENS WHEN LEFT-CLICKED
    def left_click_action(self, event):
        if self.is_mine:    # if the user left-clicked on the mine
            self.show_mine()
        #print(event)
        #print("I was left clicked")
        
        else:      # If the user left-clicked on the safe cell
            if self.surrounded_mines_length == 0:
                for cell_obj in self.surrounding:
                    if cell_obj.is_mine == False:
                        cell_obj.show_cell()
                
            #print('I am not a mine')

            self.show_cell()

            # If mines count is equal to the cells left count, player won. 
            # Need to check this after each safe click.
            if Cell.cell_count == mysettings.MINES_COUNT:
                Cell.total_cell_count_label.configure(text = f'Congratulations. You won!!')
                for cell in Cell.all:
                    cell.cell_btn.unbind('<Button-1>')
                    cell.cell_btn.unbind('<Button-2>')

        # Cancel left and right click events if the cel is already opened
        self.cell_btn.unbind('<Button-1>')
        self.cell_btn.unbind('<Button-2>')
            

    def show_mine(self):
        # A logic to interrupt the game, and display a message, that player lost.
        
        self.cell_btn.configure(text = "Mine",highlightbackground= 'yellow', fg='red')
        Cell.total_cell_count_label.configure(text = f'Game over!!!')
        Cell.game_over_flag = 1
        for cell in Cell.all:
            cell.cell_btn.unbind('<Button-1>')
            cell.cell_btn.unbind('<Button-2>')
        
        #sys.exit()   # If you want to close the window altogether after game is over.


        # GROUP OF FUNCTIONS TO CALCULATE NUMBER OF MINES AROUND THE SAFE CELL

    # A helper function to return a cell object based on the value of x and y, to achieve the above mentioned goal
    def get_cell__by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell     # exit the loop 


    @property             # This is to specify that, the next part is read-only, and cannot be modified.
    def surrounding (self):
        cells = [
            self.get_cell__by_axis(self.x-1, self.y-1),
            self.get_cell__by_axis(self.x-1, self.y),
            self.get_cell__by_axis(self.x-1, self.y+1),
            self.get_cell__by_axis(self.x, self.y-1),
            self.get_cell__by_axis(self.x, self.y+1),
            self.get_cell__by_axis(self.x+1, self.y-1),
            self.get_cell__by_axis(self.x+1, self.y),
            self.get_cell__by_axis(self.x+1, self.y+1)
        ]
        cells = [i for i in cells if i]
        return cells

    @property
    def surrounded_mines_length(self):
        counter = 0
        for cell in self.surrounding:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            #print(self.surrounded_mines_length)  
            self.cell_btn.configure(text = self.surrounded_mines_length, 
            highlightbackground='brown', bg='blue', fg='black')
            
        # replace the text of cell count label with the newer count
            if Cell.total_cell_count_label :
                Cell.total_cell_count_label.configure(text = f'Cells Left: {Cell.cell_count}')

            # If this was marked as a mine candidate, then we need to change the color to normal.
            self.cell_btn.configure(highlightbackground = 'brown')

        # Mark the cell as opened
        self.is_opened = True


         # WHEN THE USER PUTS A FLAG ON A CELL AS A MINE CANDIDATE
          # It just changes the background color, as a sign of right-click event
    def right_click_action(self, event):
        
        if not self.is_mine_candidate:
            self.is_mine_candidate = True
            self.cell_btn.configure(bg = 'orange', highlightbackground='orange')
        else: # They want to remove the red flag on this cell
            self.cell_btn.configure(bg = 'SystemButtonFace', highlightbackground='SystemButtonFace')
            self.is_mine_candidate = False

    
    # Static method to allocate the mines inside the grid. Not specific to the  cell object instance
    @staticmethod
    def randomize_mines():
        mine_cells = random.sample(Cell.all, mysettings.MINES_COUNT)
        print(mysettings.MINES_COUNT)
        
        for mine_cell in mine_cells:
            mine_cell.is_mine = True
        print(mine_cells)

   #  MODIFYING CELL REPRESENTATION

    # We will write some magic methods to change the way objects are stored in Cell.all, and is easier to understand
    def __repr__(self):
        return  f'Cell({self.x}, {self.y}, {self.is_mine})'

      # SHOW THE NUMBER OF CELLS LEFT IN THE GRID
    @staticmethod    # this is used for the class, and not for the object instance 
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = 'green',
            fg = 'white',
            highlightbackground= 'blue',
            text = f'Cells Left: {Cell.cell_count}',
            font = ("", 33)
        )
        Cell.total_cell_count_label = lbl
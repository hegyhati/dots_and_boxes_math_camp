from functools import partial
import tkinter as tk
from game import Game



class DotsAndBoxesBoard(tk.Frame):
    def __init__(self, master, game:Game):
        super().__init__(master)
        self.__game = game
        self.__master = master
        self.__load_images()
        self.__initialize_board()
    
    def __load_images(self):
        self.DISP = {
            Game.HORIZONTAL : {
                True: tk.PhotoImage(file = "gui_elements/horizontal_True.png"),
                False: tk.PhotoImage(file = "gui_elements/horizontal_False.png")
            },
            Game.VERTICAL : {
                True: tk.PhotoImage(file = "gui_elements/vertical_True.png"),
                False: tk.PhotoImage(file = "gui_elements/vertical_False.png")
            },
            "grid" : tk.PhotoImage(file = "gui_elements/grid.png"),
            "box" : {
                None: tk.PhotoImage(file = "gui_elements/box_None.png"),
                0 : tk.PhotoImage(file = "gui_elements/box_0.png"),
                1 : tk.PhotoImage(file = "gui_elements/box_1.png")
            }
        }
    
    def __initialize_board(self):        
        self.__buttons={}
        self.__boxes=[ [None] * self.__game.columns for _ in range(self.__game.rows)]
        for r in range(self.__game.rows*2+1):
            for c in range(self.__game.columns*2+1):
                if r%2==0 and c%2==0:
                    tk.Label(self, image=self.DISP["grid"]).grid(row=r, column=c)
                elif r%2==1 and c%2==1:
                    box = tk.Label(self, image=self.DISP["box"][None])
                    self.__boxes[r//2][c//2] = box
                    box.grid(row=r, column=c)
                else:
                    direction = Game.HORIZONTAL if r%2==0 else Game.VERTICAL
                    row = r//2
                    column = c//2                    
                    button = tk.Button(self, image=self.DISP[direction][False], command=partial(self.__on_click,direction,row,column))
                    self.__buttons[(direction,row,column)] = button                    
                    button.grid(row=r, column=c)
                    
    def __update_boxes(self, direction:str, row:int, column:int):
        if direction == Game.HORIZONTAL:
            if row < self.__game.rows:
                self.__boxes[row][column].config(image=self.DISP["box"][self.__game.get_box_color(row,column)])
            if row >= 1:
                self.__boxes[row-1][column].config(image=self.DISP["box"][self.__game.get_box_color(row-1,column)])
        if direction == Game.VERTICAL:
            if column < self.__game.columns:
                self.__boxes[row][column].config(image=self.DISP["box"][self.__game.get_box_color(row,column)])
            if column >= 1:
                self.__boxes[row][column-1].config(image=self.DISP["box"][self.__game.get_box_color(row,column-1)])
                    
    def __on_click(self, direction:str, row:int, column:int):
        try:
            if self.__game.move(direction,row,column):
                self.__update_boxes(direction,row,column)
            self.__buttons[(direction,row,column)].config(image=self.DISP[direction][True], relief=tk.RIDGE)
            self.__master._update()
        except ValueError as e:
            pass

class DotsAndBoxesGUI(tk.Tk):
    def __init__(self, width:int, height:int):
        super().__init__()
        self.__game = Game(width, height)
        self.score = tk.Label(self)
        self.score.pack()
        self.next = tk.Label(self, compound=tk.CENTER)
        self.next.pack()
        self.board = DotsAndBoxesBoard(self, self.__game)
        self.board.pack()
        self._player_images = [
            tk.PhotoImage(file = "gui_elements/box_0.png"),
            tk.PhotoImage(file = "gui_elements/box_1.png")
        ]
        self._update()
        
    def _update(self):
        self.score.config(text=f"Score: {self.__game.get_score()[0]} - {self.__game.get_score()[1]}")
        self.next.config(text=f"Player {self.__game.next_player()+1}'s\n turn")
        self.next.config(image=self._player_images[self.__game.next_player()])
        # adjust image size
        
        if self.__game.is_finished():
            p1,p2 = self.__game.get_score()
            if p1 == p2:
                self.next.config(text="Game Over\nIt's a draw")
                self.next.config(image=None)
            else:
                self.next.config(text=f"Game Over\nPlayer {1 if p1 > p2 else 2}\nwins.")
                self.next.config(image=self._player_images[0 if p1 > p2 else 1])
        





if __name__ == "__main__":
    width = int(input("Width of the board: "))
    height = int(input("Height of the board: "))
    
    root = DotsAndBoxesGUI(width, height)
    root.title("Simple Dots and Boxes Game")
    root.mainloop()

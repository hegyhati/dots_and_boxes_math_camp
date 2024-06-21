
DISP = {
    "horizontal" : {
        True: "━",
        False: "┄"
    },
    "vertical" : {
        True: "┃",
        False: "┆"
    },
    "grid" : "┼",
    "box" : {
        None: " ",
        0 : "█",
        1 : "▒"
    }
}

class Game:
    
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    
    def __init__(self, width = 4, height = 4) -> None:
        self._columns = width
        self._rows = height
        self._horizontal = [ [False] * width  for _ in range(height+1) ]
        self._vertical = [ [False] * (width + 1) for _ in range(height) ]
        self._color = [ [None] * width for _ in range(height) ]
        self._next = 0
        self._score = [0,0]
        self._moves_left = height * (width + 1) + (height+1) * width
    
    
    def __str__(self) -> str:
        s = [f"Player 1: {self._score[0]}, Player 2: {self._score[1]}\n"]
        for r in range(self._rows):
            for c in range(self._columns):
                s.append(DISP["grid"])
                s.append(DISP["horizontal"][self._horizontal[r][c]])
            s.append(DISP["grid"])
            s.append("\n")
            for c in range(self._columns):
                s.append(DISP["vertical"][self._vertical[r][c]])
                s.append(DISP["box"][self._color[r][c]])
            s.append(DISP["vertical"][self._vertical[r][self._columns]])
            s.append("\n")
        for c in range(self._columns):
            s.append(DISP["grid"])
            s.append(DISP["horizontal"][self._horizontal[self._rows][c]])
        s.append(DISP["grid"])
        s.append(f"\nNext player: Player {self._next+1}\n")
        return "".join(s)
    
    def _check_box(self, row:int, column:int) -> bool:
        return all((
            self._horizontal[row][column],
            self._horizontal[row+1][column],
            self._vertical[row][column],
            self._vertical[row][column+1]
        ))

    def _check_new_boxes(self,direction:str, row:int, column:int) -> int:
        new_boxes = 0
        if direction == self.HORIZONTAL:
            if row >= 1 and self._check_box(row-1,column):
                new_boxes += 1
                self._color[row-1][column] = self._next
            if row < self._rows and self._check_box(row,column):
                new_boxes += 1
                self._color[row][column] = self._next
        if direction == self.VERTICAL:
            if column >= 1 and self._check_box(row,column-1):
                new_boxes += 1
                self._color[row][column-1] = self._next
            if column < self._columns and self._check_box(row,column):
                new_boxes += 1
                self._color[row][column] = self._next      
        self._score[self._next] += new_boxes
        return new_boxes

    def is_finished(self) -> bool:
        return self._moves_left == 0
    
    def next_player(self) -> int:
        return self._next

    def move(self, direction:str, row:int, column:int) -> bool:
        where = self._horizontal if direction == self.HORIZONTAL else self._vertical
        if where[row][column]: raise ValueError("Already done")
        where[row][column] = True
        self._moves_left -= 1
        new_box = self._check_new_boxes(direction, row, column)
        if new_box == 0: self._next = 1 - self._next
        return new_box
        
            

def simple_game():       
    g = Game(3,4)
    while not g.is_finished():
        print(g)
        d = Game.HORIZONTAL if input("direction (h/v)")=="h" else Game.VERTICAL
        r = int(input("r="))
        c = int(input("c="))
        g.move(d,r,c)

if __name__ == "__main__":
    simple_game()

class Game:
    
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    
    def __init__(self, width = 4, height = 4) -> None:
        self._columns = self.columns = width
        self._rows = self.rows = height
        self._horizontal = [ [False] * width  for _ in range(height+1) ]
        self._vertical = [ [False] * (width + 1) for _ in range(height) ]
        self._color = [ [None] * width for _ in range(height) ]
        self._next = 0
        self._score = [0,0]
        self._moves_left = height * (width + 1) + (height+1) * width
    
    def _check_box(self, row:int, column:int) -> bool:
        return all((
            self._horizontal[row][column],
            self._horizontal[row+1][column],
            self._vertical[row][column],
            self._vertical[row][column+1]
        ))

    def __check_new_boxes(self,direction:str, row:int, column:int) -> int:
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
    
    def is_placed(self,direction:str, row:int, column:int) -> bool:
        where = self._horizontal if direction == self.HORIZONTAL else self._vertical
        return where[row][column]

    def get_box_color(self, row:int, column:int) -> None|int:
        return self._color[row][column]
    
    def next_player(self) -> int:
        return self._next
    
    def get_score(self) ->tuple[int]:
        return tuple(self._score)

    def move(self, direction:str, row:int, column:int) -> int:
        where = self._horizontal if direction == self.HORIZONTAL else self._vertical
        if where[row][column]: raise ValueError("Already done")
        where[row][column] = True
        self._moves_left -= 1
        new_box = self.__check_new_boxes(direction, row, column)
        if new_box == 0: self._next = 1 - self._next
        return new_box
    
   


class GameWithUndo(Game):
    def __init__(self, width=4, height=4) -> None:
        super().__init__(width, height)
        self.__moves = []

    def move(self, direction:str, row:int, column:int) -> bool:
        self.__moves.append((self._next, direction, row, column))
        return super().move(direction,row,column)


    def __uncheck_boxes(self,direction:str, row:int, column:int) -> None:
        if direction == self.HORIZONTAL:
            if row >= 1 and self._check_box(row-1,column):
                self._score[self._color[row-1][column]] -= 1
                self._color[row-1][column] = None
            if row < self._rows and self._check_box(row,column):
                self._score[self._color[row][column]] -= 1
                self._color[row][column] = None
        if direction == self.VERTICAL:
            if column >= 1 and self._check_box(row,column-1):
                self._score[self._color[row][column-1]] -= 1
                self._color[row][column-1] = None
            if column < self._columns and self._check_box(row,column):
                self._score[self._color[row][column]] -= 1
                self._color[row][column] = None
    def undo(self) -> bool:
        if len(self.__moves) == 0: raise IndexError("No moves left to undo.")
        player,direction,row,column = self.__moves.pop()
        where = self._horizontal if direction == self.HORIZONTAL else self._vertical
        self.__uncheck_boxes(direction, row, column)
        where[row][column] = False
        self._next = player
        self._moves_left += 1
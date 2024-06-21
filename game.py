
class Game:
    
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    
    def __init__(self, width = 4, height = 4) -> None:
        self.__columns = self.columns = width
        self.__rows = self.rows = height
        self.__horizontal = [ [False] * width  for _ in range(height+1) ]
        self.__vertical = [ [False] * (width + 1) for _ in range(height) ]
        self.__color = [ [None] * width for _ in range(height) ]
        self.__next = 0
        self.__score = [0,0]
        self.__moves_left = height * (width + 1) + (height+1) * width
    
    def __check_box(self, row:int, column:int) -> bool:
        return all((
            self.__horizontal[row][column],
            self.__horizontal[row+1][column],
            self.__vertical[row][column],
            self.__vertical[row][column+1]
        ))

    def __check_new_boxes(self,direction:str, row:int, column:int) -> int:
        new_boxes = 0
        if direction == self.HORIZONTAL:
            if row >= 1 and self.__check_box(row-1,column):
                new_boxes += 1
                self.__color[row-1][column] = self.__next
            if row < self.__rows and self.__check_box(row,column):
                new_boxes += 1
                self.__color[row][column] = self.__next
        if direction == self.VERTICAL:
            if column >= 1 and self.__check_box(row,column-1):
                new_boxes += 1
                self.__color[row][column-1] = self.__next
            if column < self.__columns and self.__check_box(row,column):
                new_boxes += 1
                self.__color[row][column] = self.__next      
        self.__score[self.__next] += new_boxes
        return new_boxes

    def is_finished(self) -> bool:
        return self.__moves_left == 0
    
    def is_placed(self,direction:str, row:int, column:int) -> bool:
        where = self.__horizontal if direction == self.HORIZONTAL else self.__vertical
        return where[row][column]

    def get_box_color(self, row:int, column:int) -> None|int:
        return self.__color[row][column]
    
    def next_player(self) -> int:
        return self.__next
    
    def get_score(self) ->tuple[int]:
        return tuple(self.__score)

    def move(self, direction:str, row:int, column:int) -> bool:
        where = self.__horizontal if direction == self.HORIZONTAL else self.__vertical
        if where[row][column]: raise ValueError("Already done")
        where[row][column] = True
        self.__moves_left -= 1
        new_box = self.__check_new_boxes(direction, row, column)
        if new_box == 0: self.__next = 1 - self.__next
        return new_box     

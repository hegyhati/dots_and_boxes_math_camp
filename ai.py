import torch
import torch.nn as nn
from game import Game



class AI_player:
    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height
        self.size = width*(height+1) + (width+1)*height
        self.model = nn.Sequential(
            nn.Linear(self.size, self.size//2),  
            nn.ReLU(),    
            nn.Linear(self.size//2, self.size//4),
            nn.ReLU(),
            nn.Linear(self.size//4, self.size),
        )        
        
    def __idx_to_move(self, idx:int) -> tuple:
        if idx < self.width*(self.height+1):
            return Game.HORIZONTAL, idx // self.width, idx % self.width
        else:
            idx -= self.width*(self.height+1)
            return Game.VERTICAL, idx // (self.width+1), idx % (self.width+1)
        
    def __get_input(self, game:Game) -> torch.Tensor:
        input = torch.zeros(self.size)
        for idx in range(self.size):
            if game.is_placed(*self.__idx_to_move(idx)):
                input[idx] = 1
        return input
    
    def get_moves(self, game:Game) -> list[tuple]:
        input = self.__get_input(game)
        output = self.model(input)
        sorted_indices = torch.argsort(output, descending=True)
        return [self.__idx_to_move(idx) for idx in sorted_indices]
    
    def mutate(self, mutation_rate:float):
        for layer in self.model:
            if isinstance(layer, nn.Linear):
                for param in layer.parameters():
                    param.data += torch.randn_like(param) * mutation_rate


from text_ui import board_str

width = int(input("Width of the board: "))
height = int(input("Height of the board: "))
ai = AI_player(width, height)
game = Game(width, height)
score = 0
while not game.is_finished():
    while not game.is_finished():
        print(board_str(game))
        moves = ai.get_moves(game)
        for move in moves:
            try:
                boxes = game.move(*move)
                print(f"AI moves with {move[0],int(move[1]), int(move[2])} (Score: {score})")
                break
            except ValueError:
                score -= 1
        if boxes == 0:
            break
    while not game.is_finished():
        print(board_str(game))
        d,r,c = input(f"Next move (Format: h/v row column) for Player {game.next_player()+1}: ").split()
        d = Game.HORIZONTAL if d.strip()=="h" else Game.VERTICAL
        r = int(r)
        c = int(c)
        try:        
            if game.move(d,r,c) == 0:
                break
        except ValueError as e:
            print(e)
print(board_str(game))
print(game.get_score(),score)




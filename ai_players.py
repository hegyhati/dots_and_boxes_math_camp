from typing import Generator
import torch
import torch.nn as nn
from executer import Player, GameExecuter
from game import Game

class NextMovePlayer(Player):
    
   def moves(self, game: Game) -> Generator[tuple[str, int, int], None, None]:
        for d in [Game.HORIZONTAL, Game.VERTICAL]:
            for r in range(game.height+1 if d == Game.HORIZONTAL else game.height):
                for c in range(game.width if d == Game.HORIZONTAL else game.width+1):
                    if not game.is_placed(d,r,c):
                        yield d,r,c
    
    
class NeuralNetworkPlayer(Player):
    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height
        self.size = width*(height+1) + (width+1)*height
        self.model = nn.Sequential(
            nn.Linear(self.size, self.size*2),  
            nn.ReLU(),    
            nn.Linear(self.size*2, self.size*2),
            nn.ReLU(),
            nn.Linear(self.size*2, self.size),
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
    
    def moves(self, game: Game) -> Generator[tuple[str, int, int], None, None]:
        input = self.__get_input(game)
        output = self.model(input)
        sorted_indices = torch.argsort(output, descending=True)
        for idx in sorted_indices:
            move = self.__idx_to_move(idx)
            yield move
    
    def mutate(self, mutation_rate:float):
        for layer in self.model:
            if isinstance(layer, nn.Linear):
                for param in layer.parameters():
                    param.data += torch.randn_like(param) * mutation_rate

def PvAI():
    from human_text_player import HumanTextPlayer
    player1 = HumanTextPlayer()    
    width = int(input("Width of the board: "))
    height = int(input("Height of the board: "))
    computer = input("Which AI you would like to play against? (NextMove/NeuralNetwork): ")
    if computer == "NextMove":
        player2 = NextMovePlayer()
    elif computer == "NeuralNetwork":
        player2 = NeuralNetworkPlayer(width, height)
    executer = GameExecuter(player1, player2,width, height)
    executer.execute()

if __name__ == '__main__':
    PvAI()
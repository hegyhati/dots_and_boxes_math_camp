import random
from typing import Generator
import torch
import torch.nn as nn
from executer import Player, GameExecuter
from game import Game
from copy import deepcopy

class NextMovePlayer(Player):
    
   def moves(self, game: Game) -> Generator[tuple[str, int, int], None, None]:
        for d in [Game.HORIZONTAL, Game.VERTICAL]:
            for r in range(game.height+1 if d == Game.HORIZONTAL else game.height):
                for c in range(game.width if d == Game.HORIZONTAL else game.width+1):
                    if not game.is_placed(d,r,c):
                        yield d,r,c

class RandomPlayer(Player):
    
   def moves(self, game: Game) -> Generator[tuple[str, int, int], None, None]:
        directions = [Game.HORIZONTAL, Game.VERTICAL]
        random.shuffle(directions)
        for d in directions:
            rows = list(range(game.height+1 if d == Game.HORIZONTAL else game.height))
            random.shuffle(rows)
            columns = list(range(game.width if d == Game.HORIZONTAL else game.width+1))
            random.shuffle(columns)
            for r in rows:
                for c in columns:
                    if not game.is_placed(d,r,c):
                        yield d,r,c
    
    
class NeuralNetworkPlayer(Player):
    def __init__(self, width:int, height:int, mutationrate = 0.1, hidden_layer_size_multipliers = [0.7, 0.7]) -> None:
        self.width = width
        self.height = height
        self.size = width*(height+1) + (width+1)*height
        layersizes = [self.size] + [int(self.size * multiplier) for multiplier in hidden_layer_size_multipliers] + [self.size]
        self.model = nn.Sequential()
        for i in range(len(layersizes)-1):
            self.model.add_module(f'linear{i}', nn.Linear(layersizes[i], layersizes[i+1]))
            if i < len(layersizes)-2:
                self.model.add_module(f'relu{i}', nn.ReLU())
        self._score = 0
        self.mutationrate = mutationrate
        
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
            self._score -= 1
    
    def mutate(self):
        for layer in self.model:
            if isinstance(layer, nn.Linear):
                for param in layer.parameters():
                    param.data += torch.randn_like(param) * self.mutationrate
    
    def get_child(self) -> 'NeuralNetworkPlayer':
        child = deepcopy(self)
        child.mutate()
        return child

    @staticmethod
    def get_crossover_child(parent1:'NeuralNetworkPlayer', parent2:'NeuralNetworkPlayer') -> 'NeuralNetworkPlayer':
        child = deepcopy(parent1)
        for layer1,layer2 in zip(parent1.model, parent2.model):
            if isinstance(layer1, nn.Linear):
                for param1,param2 in zip(layer1.parameters(), layer2.parameters()):
                    match random.choice([1,2,3]):
                        case 1:
                            param1.data = param1.data
                        case 2:
                            param1.data = param2.data
                        case 3:
                            param1.data = (param1.data + param2.data) / 2 
        return child
    
    def on_win(self, game:Game, **kargs) -> None:
        p1,p2 = game.get_score()
        self._score += max(p1,p2)-min(p1,p2)
    
    def on_lose(self, game:Game, **kargs) -> None:
        p1,p2 = game.get_score()
        self._score += min(p1,p2)-max(p1,p2)

    def reset_score(self) -> None:
        self._score = 0
    
    def get_score(self) -> int:
        return self._score
    
    def pretrain_with(self, PlayerClass, max_iteration:int = 100, max_worsen = 10) -> list[int]:
        nmp = PlayerClass()
        self.reset_score()
        GameExecuter(nmp, self, self.width, self.height).execute()
        lastbest_dict = self.model.state_dict()
        lastbestscore = self.get_score()
        scores = [lastbestscore]
        worsen = 0
        while scores[-1] < 2 and len(scores) < max_iteration:
            if scores[-1] < lastbestscore:
                worsen += 1
                if worsen > max_worsen:
                    self.model.load_state_dict(lastbest_dict)
                    scores.append(f"RESET to {lastbestscore}")
            else:
                lastbestscore = scores[-1]
                lastbest_dict = self.model.state_dict()
            self.mutate()
            self.reset_score()
            GameExecuter(nmp, self, self.width, self.height).execute()
            scores.append(self.get_score())
        self.model.load_state_dict(lastbest_dict)
        self.reset_score()
        scores.append(f"BEST: {lastbestscore}")
        return scores
            
        

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
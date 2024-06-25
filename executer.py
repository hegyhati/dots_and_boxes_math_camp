from typing import Generator
from game import Game

class Player:
    def moves(self, game:Game) -> Generator[tuple[str,int,int], None, None]:
        raise NotImplementedError()
    
    def on_win(self, game:Game, **kargs) -> None:
        raise NotImplementedError()
    
    def on_lose(self, game:Game, **kargs) -> None:
        raise NotImplementedError()


class GameExecuter:
    def __init__(self, player1:player, player2:player, width:int, height:int) -> None:
        self.game = Game(width, height)
        self.players = [player1, player2]
        
    def execute(self) -> int:
        while not self.game.is_finished():
            player = self.players[self.game.next_player()]
            for move in player.move(self.game):
                try:
                    self.game.move(*move)
                    break
                except ValueError:
                    pass
        p1,p2 = self.game.get_score()
        if p1 > p2:
            self.players[0].on_win(self.game)
            self.players[1].on_lose(self.game)
        elif p2 > p1:
            self.players[1].on_win(self.game)
            self.players[0].on_lose(self.game)
        return p1-p2
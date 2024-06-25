from typing import Generator
from game import Game

class Player:
    def moves(self, game:Game) -> Generator[tuple[str,int,int], None, None]:
        raise NotImplementedError()
    
    def on_win(self, game:Game, **kargs) -> None:
        pass
    
    def on_lose(self, game:Game, **kargs) -> None:
        pass


class GameExecuter:
    def __init__(self, player1:Player, player2:Player, width:int, height:int) -> None:
        self.game = Game(width, height)
        self.players = [player1, player2]
        
    def execute(self, verbose=False) -> int:
        while not self.game.is_finished():
            if verbose: 
                print(HumanTextPlayer.score_str(self.game))
                print(HumanTextPlayer.board_str(self.game))
            player = self.players[self.game.next_player()]
            for move in player.moves(self.game):
                try:
                    if verbose: print(f"Player {self.game.next_player()} tries: {move}")
                    self.game.move(*move)
                    break
                except ValueError:
                    pass
        if verbose: 
            print(HumanTextPlayer.score_str(self.game))
            print(HumanTextPlayer.board_str(self.game))
        p1,p2 = self.game.get_score()
        if p1 > p2:
            if verbose: print(f"Player 1 wins! {p1} - {p2}")
            self.players[0].on_win(self.game)
            self.players[1].on_lose(self.game)
        elif p2 > p1:
            if verbose: print(f"Player 2 wins! {p1} - {p2}")
            self.players[1].on_win(self.game)
            self.players[0].on_lose(self.game)
        return p1-p2
    
    
    

if __name__ == "__main__":
    import argparse
    from human_text_player import HumanTextPlayer
    from ai_players import NextMovePlayer, NeuralNetworkPlayer
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", type=str, help="Player 1 (Human/NextMove/NeuralNetwork)")
    parser.add_argument("player2", type=str, help="Player 2 (Human/NextMove/NeuralNetwork)")
    parser.add_argument("width", type=int, help="Width of the game board")
    parser.add_argument("height", type=int, help="Height of the game board")
    args = parser.parse_args()
    
    player1 = HumanTextPlayer() if args.player1 == "Human" else NextMovePlayer() if args.player1 == "NextMove" else NeuralNetworkPlayer(args.width, args.height)
    player2 = HumanTextPlayer() if args.player2 == "Human" else NextMovePlayer() if args.player2 == "NextMove" else NeuralNetworkPlayer(args.width, args.height)
    
    executer = GameExecuter(player1, player2, args.width, args.height)
    executer.execute(verbose=True)
    
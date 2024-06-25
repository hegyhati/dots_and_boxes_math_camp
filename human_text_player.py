from game import Game
from executer import Player
from typing import Generator
from game_text_ui import GameTextUI

class HumanTextPlayer(Player):
    
    def moves(self, game:Game) -> Generator[tuple[str,int,int], None, None]:
        print(GameTextUI.score_str(game,game.next_player()) + GameTextUI.board_str(game))
        while True:   
            try:
                moves = GameTextUI.get_move_input(game)
                print() 
            except ValueError as e:
                print(e, "Try again")
                continue
            yield moves

    def on_win(self, game:Game, **kargs) -> None:
        print("You win!")
        print(GameTextUI.board_str(game))
    
    def on_lose(self, game:Game, **kargs) -> None:
        print("You lose!")
        print(GameTextUI.board_str(game))
        
    def on_draw(self, game: Game, **kargs) -> None:
        print("It's a draw!")
        print(GameTextUI.board_str(game))
        

def PvP():
    from executer import GameExecuter
    width = int(input("Width of the board: "))
    height = int(input("Height of the board: "))
    p1 = HumanTextPlayer()
    p2 = HumanTextPlayer()
    g = GameExecuter(p1,p2,width,height)
    g.execute()

if __name__ == "__main__":
    PvP()
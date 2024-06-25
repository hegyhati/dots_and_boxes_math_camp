from game import Game
from executer import Player, GameExecuter
from typing import Generator

class HumanTextPlayer(Player):
    
    DISP = {
        "horizontal" : {
            True: "━━",
            False: "┈┈"
        },
        "vertical" : {
            True: "┃",
            False: "┊"
        },
        "grid" : "╋",
        "box" : {
            None: "  ",
            0 : "██",
            1 : "░░"
        }
    }

    @staticmethod
    def score_str(game:Game, player:int|None = None) -> str:
        return f"Player 1{'(YOU)' if player == 0 else ''}: {game.get_score()[0]}, Player 2{'(YOU)' if player == 1 else ''}: {game.get_score()[1]}\n"

    @staticmethod
    def board_str(game:Game) -> str:
        s = []
        for r in range(game.height):
            for c in range(game.width):
                s.append(HumanTextPlayer.DISP["grid"])
                s.append(HumanTextPlayer.DISP["horizontal"][game.is_placed(Game.HORIZONTAL,r,c)])
            s.append(HumanTextPlayer.DISP["grid"])
            s.append("\n")
            for c in range(game.width):
                s.append(HumanTextPlayer.DISP["vertical"][game.is_placed(Game.VERTICAL,r,c)])
                s.append(HumanTextPlayer.DISP["box"][game.get_box_color(r,c)])
            s.append(HumanTextPlayer.DISP["vertical"][game.is_placed(Game.VERTICAL,r,game.width)])
            s.append("\n")
        for c in range(game.width):
            s.append(HumanTextPlayer.DISP["grid"])
            s.append(HumanTextPlayer.DISP["horizontal"][game.is_placed(Game.HORIZONTAL,game.height,c)])
        s.append(HumanTextPlayer.DISP["grid"])
        s.append(f"\n")
        return "".join(s)
    
    @staticmethod
    def _textinput_to_move(text:str, game:Game) -> tuple[str,int,int]:
        d,r,c = text.split()
        try:
            r = int(r)
            c = int(c)
        except ValueError:
            raise ValueError("Invalid row or column input.")
        if d.strip() not in "hv":
            raise ValueError("Invalid direction input.")
        d = Game.HORIZONTAL if d.strip()=="h" else Game.VERTICAL
        if not game.is_valid_move(d,r,c):
            raise ValueError("Move out of bounds.")
        return d,r,c

    def moves(self, game:Game) -> Generator[tuple[str,int,int], None, None]:
        print(HumanTextPlayer.score_str(game,game.next_player()) + HumanTextPlayer.board_str(game))
        while True:   
            try:
                moves = HumanTextPlayer._textinput_to_move(input(f"Next move (Format: h/v row column): "), game)
                print() 
            except ValueError as e:
                print(e, "Try again")
                continue
            yield moves

    def on_win(self, game:Game, **kargs) -> None:
        print("You win!")
        print(HumanTextPlayer.board_str(game))
    
    def on_lose(self, game:Game, **kargs) -> None:
        print("You lose!")
        print(HumanTextPlayer.board_str(game))
        
    def on_draw(self, game: Game, **kargs) -> None:
        print("It's a draw!")
        print(HumanTextPlayer.board_str(game))
        

def PvP():
    width = int(input("Width of the board: "))
    height = int(input("Height of the board: "))
    p1 = HumanTextPlayer()
    p2 = HumanTextPlayer()
    g = GameExecuter(p1,p2,width,height)
    g.execute()

if __name__ == "__main__":
    PvP()
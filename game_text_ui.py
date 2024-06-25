from game import Game

class GameTextUI:
    
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
                s.append(GameTextUI.DISP["grid"])
                s.append(GameTextUI.DISP["horizontal"][game.is_placed(Game.HORIZONTAL,r,c)])
            s.append(GameTextUI.DISP["grid"])
            s.append("\n")
            for c in range(game.width):
                s.append(GameTextUI.DISP["vertical"][game.is_placed(Game.VERTICAL,r,c)])
                s.append(GameTextUI.DISP["box"][game.get_box_color(r,c)])
            s.append(GameTextUI.DISP["vertical"][game.is_placed(Game.VERTICAL,r,game.width)])
            s.append("\n")
        for c in range(game.width):
            s.append(GameTextUI.DISP["grid"])
            s.append(GameTextUI.DISP["horizontal"][game.is_placed(Game.HORIZONTAL,game.height,c)])
        s.append(GameTextUI.DISP["grid"])
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
    
    @staticmethod
    def get_move_input(game:Game) -> tuple[str,int,int]:
        return GameTextUI._textinput_to_move(input(f"Next move (Format: h/v row column): "), game)
    

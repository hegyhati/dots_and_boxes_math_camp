from game import Game

DISP = {
    "horizontal" : {
        True: "━━",
        False: "┄┄"
    },
    "vertical" : {
        True: "┃",
        False: "┆"
    },
    "grid" : "┼",
    "box" : {
        None: "  ",
        0 : "██",
        1 : "▒▒"
    }
}

def board_str(game:Game) -> str:
    s = [f"Player 1: {game.get_score()[0]}, Player 2: {game.get_score()[1]}\n"]
    for r in range(game.rows):
        for c in range(game.columns):
            s.append(DISP["grid"])
            s.append(DISP["horizontal"][game.is_placed(Game.HORIZONTAL,r,c)])
        s.append(DISP["grid"])
        s.append("\n")
        for c in range(game.columns):
            s.append(DISP["vertical"][game.is_placed(Game.VERTICAL,r,c)])
            s.append(DISP["box"][game.get_box_color(r,c)])
        s.append(DISP["vertical"][game.is_placed(Game.VERTICAL,r,game.columns)])
        s.append("\n")
    for c in range(game.columns):
        s.append(DISP["grid"])
        s.append(DISP["horizontal"][game.is_placed(Game.HORIZONTAL,game.rows,c)])
    s.append(DISP["grid"])
    s.append(f"\n")
    return "".join(s)

def game(width, height):
    g = Game(width,height)
    while not g.is_finished():
        print(board_str(g))
        while True:
            d,r,c = input(f"Next move (Format: h/v row column) for Player {g.next_player()+1}: ").split()
            d = Game.HORIZONTAL if d.strip()=="h" else Game.VERTICAL
            r = int(r)
            c = int(c)
            try:        
                g.move(d,r,c)
                break
            except ValueError as e:
                print(e)
    
    print(board_str(g))
    

if __name__ == "__main__":
    height = int(input("Height of board: "))
    width  = int(input("Width of board: "))
    game(width, height)
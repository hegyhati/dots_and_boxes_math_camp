from game import GameWithUndo

def get_all_moves(width:int, height:int) -> list[tuple]:
    return [ 
            (GameWithUndo.HORIZONTAL, r, c) 
            for r in range(height+1) for c in range(width)
    ] + [
            (GameWithUndo.VERTICAL, r, c)
            for r in range(height) for c in range(width+1)
    ]


def solve(game:GameWithUndo, moves:list[tuple]) -> int:
    if game.is_finished():
        p1,p2 = game.get_score()
        return p1-p2
    func = max if game.next_player() == 0 else min
    results = []
    for idx,move in enumerate(moves):
        game.move(*move)
        results.append(solve(game,moves[:idx]+moves[idx+1:]))
        game.undo()
    return func(results)


def clever_solve(game:GameWithUndo, moves:list[tuple], parent_current_best=None, parent_current_worst=None) -> int:
    p1,p2 = game.get_score()
    remaining = totalboxes-p1-p2
    best = p1-p2 + remaining
    worst = p1-p2 - remaining
    if parent_current_best and parent_current_best > best: return -1 *  totalboxes
    if parent_current_worst and parent_current_worst < worst: return -1 * totalboxes
    
    
    func,bound,init = (max,"best",worst) if game.next_player() == 0 else (min,"worst",best)
    
    results = [init]
    parent = {
        "parent_current_best" : parent_current_best,
        "parent_current_worst" : parent_current_worst,
    }
    for idx,move in enumerate(moves):
        game.move(*move)
        if func == min and parent_current_worst:
            parent["parent_current_worst"] = min(parent_current_worst, *results)
        elif func == max and parent_current_best:
            parent["parent_current_best"] = max(parent_current_best, *results)
        results.append(clever_solve(game,moves[:idx]+moves[idx+1:], **parent))
        game.undo()
    return func(results)


from sys import argv
size = int(argv[1]), int(argv[2])
totalboxes = size[0]*size[1]
g = GameWithUndo(*size)
m = get_all_moves(*size)
print(clever_solve(g,m))
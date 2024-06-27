import pickle
from game import Game
from ai_players import NextMovePlayer, NeuralNetworkPlayer
from executer import GameExecuter

PLAYER_COUNT = 64
MUTATED_PLAYER_COUNT = 16
NEW_CHILD_COUNT = 15

SIZE = 3,3
NN_OPTIONS = {
    "mutationrate": 0.15,
    "hidden_layer_size_multipliers": [2,2.1,1.2,1]
}
PRE_TRAINING_OPTIONS = {
    "max_iteration": 50,
    "max_worsen": 5
}
TRAINING_ROUNDS = 50

players = [
    NeuralNetworkPlayer(*SIZE, **NN_OPTIONS)
    for _ in range(PLAYER_COUNT)
]

for player in players:
    scores = player.pretrain_with_nextmove(**PRE_TRAINING_OPTIONS)
    print(scores[-1])

counter = 0
while True:
    counter += 1
    scores = [0] * PLAYER_COUNT
    for idx1 in range(PLAYER_COUNT):
        for idx2 in range(PLAYER_COUNT):
            if idx1 == idx2: continue
            players[idx1].reset_score()
            players[idx2].reset_score()
            GameExecuter(players[idx1],players[idx2],*SIZE).execute()
            scores[idx1] += players[idx1].get_score()
            scores[idx2] += players[idx2].get_score()
    print(sum(scores), end=" ")
    rank = list(zip(scores,players,range(PLAYER_COUNT)))
    rank.sort(key=lambda x: x[0], reverse=True)   
    print([round(x[0],2) for x in rank[:10]])
    if counter % 10 == 0:
        filename = f"saves_11o/nn_{counter:04}_{sum(scores)}_{rank[0][0]}.pickle"
        with open(filename, "wb") as f:
            pickle.dump(rank[0][1], f)
    for i in range(MUTATED_PLAYER_COUNT):
        rank[-i-NEW_CHILD_COUNT-1][1].mutate()
    for i in range(NEW_CHILD_COUNT):
        players[rank[-i-1][2]] = rank[i][1].get_child()
    
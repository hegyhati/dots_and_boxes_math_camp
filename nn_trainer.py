import datetime
import os
import pickle
import random
from game import Game
from ai_players import RandomPlayer, NeuralNetworkPlayer
from executer import GameExecuter

PLAYER_COUNT = 50
ELITE_PLAYER_COUNT = 30
CROSSOVER_PLAYER_COUNT = 10
MUTATED_CHILD_COUNT = 5
RANDOM_PLAYER_COUNT = 5

SIZE = 3,3
NN_OPTIONS = {
    "mutationrate": 0.05,
    "hidden_layer_size_multipliers": [2,2.1,1.2]
}
PRE_TRAINING_OPTIONS = {
    "max_iteration": 1000,
    "max_worsen": 10
}

players = [
    NeuralNetworkPlayer(*SIZE, **NN_OPTIONS)
    for _ in range(PLAYER_COUNT)
]

for player in players:
    scores = player.pretrain_with(RandomPlayer, **PRE_TRAINING_OPTIONS)
    print(scores[-1])

counter = 0
time = datetime.datetime.now().isoformat()
dirname = f"saves/{time}/"
os.makedirs(dirname, exist_ok=True)

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
    if counter % 100 == 0:
        filename = os.path.join(dirname, f"nn_{counter:06}_{sum(scores)}_{rank[0][0]}.pickle")
        with open(filename, "wb") as f:
            pickle.dump(rank, f)
    new_players = [rank[i][1] for i in range(ELITE_PLAYER_COUNT)]
    for i in range(MUTATED_CHILD_COUNT):
        new_players.append(rank[i][1].get_child())
    for i in range(CROSSOVER_PLAYER_COUNT):
        parent1 = random.choice(rank[:ELITE_PLAYER_COUNT])[1]
        parent2 = random.choice(rank[:ELITE_PLAYER_COUNT])[1]
        new_players.append(NeuralNetworkPlayer.get_crossover_child(parent1, parent2))
    for i in range(RANDOM_PLAYER_COUNT):
        new_players.append(NeuralNetworkPlayer(*SIZE, **NN_OPTIONS))
    players = new_players
    
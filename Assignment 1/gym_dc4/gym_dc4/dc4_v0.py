import gym
import gym_dc4.gym_dc4.envs
import random
from DC4.DynamicConnect4 import game


def create_action_vector():
    return {"x1": False, "x2": False,
            "x3": False, "x4": False,
            "x5": False, "x6": False,
            "o1": False, "o2": False,
            "o3": False, "o4": False,
            "o5": False, "o6": False,
            "N": False, "S": False,
            "E": False, "W": False}


def generate_action(board, player, observation):
    moves = game.move(board, player)
    move = random.choice(moves)
    peon = observation["board"][move[0]][move[1]]
    action = create_action_vector()
    action[peon] = True
    action[move[2]] = True
    return action

game = game()
board = game.board
player = True

env = gym.make('dc4-v0')
for i_episode in range(100):
    observation = env.reset()
    for t in range(100):
        env.render()
        action = generate_action(board, player, observation)
        observation, reward, done, info = env.step(action)
        player = not player
        if done:
            print("Episode finished after {} timesteps".format(t + 1))
            break




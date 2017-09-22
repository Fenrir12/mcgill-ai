import tensorflow as tf
import tensorflow.contrib.slim as slim
import gym
import gym_dc4.gym_dc4.envs
import random
import numpy as np
import matplotlib.pyplot as plt
from DC4.DynamicConnect4 import game

try:
    xrange = xrange
except:
    xrange = range


def create_action_vector():
    return {"x1": False, "x2": False,
            "x3": False, "x4": False,
            "x5": False, "x6": False,
            "o1": False, "o2": False,
            "o3": False, "o4": False,
            "o5": False, "o6": False,
            "N": False, "S": False,
            "E": False, "W": False}


def all_actions_decoded():
    pieces = []
    actions = []
    for color in ['x', 'o']:
        for i in ['1', '2', '3', '4', '5', '6']:
            pieces.append(color+i)
    for piece in pieces:
        for dir in ['N', 'S', 'E', 'W']:
            a = create_action_vector()
            a[piece]= True
            a[dir] = True
            actions.append(a)
    return actions


def encode_state(s):
    encoded = [1.0] if s["player"] == 'X' else [0.0]
    for row in s['board']:
        for col in row:
            if col == 'x1':
                encoded+=([1.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'x2':
                encoded+=([0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'x3':
                encoded+=([0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'x4':
                encoded+=([0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'x5':
                encoded+=([0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'x6':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'o1':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'o2':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
            elif col == 'o3':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
            elif col == 'o4':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
            elif col == 'o5':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
            elif col == 'o6':
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
            else:
                encoded+=([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return encoded


def generate_action(board, player, observation):
    moves = game.move(board, player)
    move = random.choice(moves)
    peon = observation["board"][move[0]][move[1]]
    action = create_action_vector()
    action[peon] = True
    action[move[2]] = True
    return action


env = gym.make('dc4-v0')
env.reset()

tf.reset_default_graph()


#These lines establish the feed-forward part of the network used to choose actions
inputs1 = tf.placeholder(shape=[1, 49*12+1],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([49*12+1, 48], 0, 0.01))
Qout = tf.matmul(inputs1, W)
predict = tf.argmax(Qout, 1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1, 48], dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)



init = tf.initialize_all_variables()

# Set learning parameters
y = .99
e = 0.2
num_episodes = 500000
# create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        # Reset environment and get first new observation
        s = encode_state(env.reset())
        rAll = 0
        d = False
        j = 0
        all_actions = all_actions_decoded()

        # The Q-Network
        while j < 99:
            j += 1
            # Choose an action by greedily (with e chance of random action) from the Q-network
            a, allQ = sess.run([predict, Qout], feed_dict={inputs1: [s]})
            action = all_actions[a[0]]
            if np.random.rand(1) < e:
                action = random.choice(all_actions)
            # Get new state and reward from environment
            s1, d, r, _ = env.step(action)
            # Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout, feed_dict={inputs1: [encode_state(s1)]})
            # Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0, a[0]] = r + y*maxQ1
            # Train our network using target and predicted Q values
            _, W1 = sess.run([updateModel, W], feed_dict={inputs1: [encode_state(s1)], nextQ: targetQ})
            rAll += r
            s = encode_state(s1)
            if d == True:
                # Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                env.render()
                with open("test.txt", "a") as myfile:
                    myfile.write('Reward is '+str(rAll))
                break

        jList.append(j)
        rList.append(rAll)
print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")
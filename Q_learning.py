import numpy as np
import random

gamma = 0.9
alpha = 0.1
epsilon = 0.1


# game rules
def initialize_environment(dimensions, snakes, ladders, dragon, genie, phoenix, diamond):
    n_states = dimensions * dimensions
    goal = n_states - 1
    return n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond


def get_reward(state, diamond_collected, goal, snakes, ladders, dragon, genie, phoenix, diamond) : #rewards
    if state == goal:
        return 100
    elif state in snakes:
        return -10
    elif state in ladders:
        return 10
    elif state == dragon and not diamond_collected:
        return -50
    elif state == genie or state == phoenix:
        return 10
    else:
        return -1

def next_state(state, action, n_states, snakes, ladders, dragon, genie, phoenix, diamond, diamond_collected):
    if action == 0:
        next_state = state - 1
    elif action == 1:
        next_state = state + 1
    elif action == 2:
        next_state = state - 2
    elif action == 3:
        next_state = state + 2
    else:
        next_state = state

    next_state = max(0, min(next_state, n_states - 1))

    #backward movement
    if random.uniform(0, 1) < 0.2:
        if action == 0:
            next_state = state + 1
        elif action == 1:
            next_state = state - 1
        elif action == 2:
            next_state = state + 2
        elif action == 3:
            next_state = state - 2
        next_state = max(0, min(next_state, n_states - 1))

    if next_state in snakes:
        next_state = snakes[next_state]
    elif next_state in ladders:
        next_state = ladders[next_state]
    elif next_state == dragon and not diamond_collected:
        next_state = 0
    elif next_state == genie:
        next_state = max(0, 100 - (next_state % 10))
    elif next_state == phoenix:
        next_state = min(n_states - 1, next_state + (10 - (next_state % 10)))

    return next_state


# Q-learning
def q_learning(n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond):
    q_table = np.zeros((n_states, 4))
    for episode in range(10000):
        state = 0
        diamond_collected = False
        while state != goal:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(q_table[state])

            next_state_val = next_state(state, action, n_states, snakes, ladders, dragon, genie, phoenix, diamond,
                                        diamond_collected)

            if next_state_val == diamond:
                diamond_collected = True

            reward = get_reward(next_state_val, diamond_collected, goal, snakes, ladders, dragon, genie, phoenix,
            diamond)
            q_table[state, action] = q_table[state, action] + alpha * (
                        reward + gamma * np.max(q_table[next_state_val]) - q_table[state, action])
            state = next_state_val
    return q_table

#result
def display_results(q_table, n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond):
    state = 0
    diamond_collected = False
    steps = []

    while state != goal:
        action = np.argmax(q_table[state])
        next_state_val = next_state(state, action, n_states, snakes, ladders, dragon, genie, phoenix, diamond,
                                    diamond_collected)

        if next_state_val == diamond:
            diamond_collected = True

        steps.append((state, action, next_state_val))
        state = next_state_val

    print("number of steps:", len(steps))
    print("movements: ")
    for step in steps:
        initial_state, action, final_state = step
        direction = "forward" if action % 2 == 1 else "backward"
        step_size = 1 if action < 2 else 2
        correctness = "correct" if final_state == next_state(initial_state, action, n_states, snakes, ladders, dragon,
                                                          genie, phoenix, diamond, diamond_collected) else "incorrect"
        print(f"current location: {initial_state + 1 }")
        print(f"agent decision: {step_size} step/steps to {direction}")
        print(f"correctness: {correctness} move")
        print(f"new location: {final_state + 1 }")
        print("---------------------------------------------------")


dimensions = 10
snakes = {32: 4, 65: 11, 55: 19, 42: 23, 77: 58, 95: 71}
ladders = {6: 35, 20: 57, 30: 50, 62: 81}
dragon = 51
genie = 47
phoenix = 63
diamond = 40
'''
dimensions = int(input("dimensions: "))

ladders = {}
n = int(input("number of ladders:"))               
for i in range (0,n) :            
    ladder_loc1, ladder_loc2 = input(f"write location of ladder {i+1} :").split(":")
    ladders[ladder_loc1] = (ladder_loc2)
    ladder_loc2 = int(ladder_loc2) - 1
    ladder_loc1 = int(ladder_loc1) - 1
snakes = {}  
m = int(input("number of snakes:"))
for i in range(0,m):
    snake_loc1, snake_loc2 = input(f"write location of snake {i+1}:").split(":")
    snake_loc1 = int(snake_loc1) - 1
    snake_loc2 = int(snake_loc2) - 1
    snakes[snake_loc1] = snake_loc2
   
dragon = (int(input("dragon: "))) - 1
genie = (int(input("genie: "))) - 1
phoenix = (int(input("phoenix: "))) - 1
diamond = (int(input("diamond: "))) - 1
'''''
n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond = initialize_environment(dimensions, snakes, ladders,
                                                                                          dragon, genie, phoenix, diamond)
q_table = q_learning(n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond)
display_results(q_table, n_states, goal, snakes, ladders, dragon, genie, phoenix, diamond)

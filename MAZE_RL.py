import pygame
import numpy as np
import random
from matplotlib import pyplot as plt
import time



f = open("/home/amirhosein/PycharmProjects/IS_HW4/ENV1", "r")
data = [list(line.strip()) for line in f.readlines()]
fdata=[]
final_path=[]
for i in range(len(data)):
    temp= list(filter(lambda a: a != ",", data[i]))
    fdata.append(temp)
for i in range(len(data)):
    temp= list(filter(lambda a: a != ",", data[i]))
    final_path.append(temp)

Row=(len(fdata))
Column=(len(fdata[0]))

cells={"red":[],"white":[]}
Qvals=[]
for i in range(Row):
    Qvals.append([])
    for j in range(Column):
        Qvals[i].append({"u":0, "d":0, "r":0, "l":0})
        if fdata[i][j] == "1":
            cells["start"]= (i, j)
        if fdata[i][j] == "3":
            cells["goal"] = (i, j)
        if fdata[i][j] == "0":
            cells["white"].append((i, j))
        if fdata[i][j] == "2":
            cells["red"].append((i, j))

def next_moves(current):
    global Row
    global Column
    actions = ["l", "r", "u", "d"]
    if current[0] == 0:
        actions.remove("u")
    if current[0] == Row - 1:
        actions.remove("d")
    if current[1] == 0:
        actions.remove("l")
    if current[1] == Column - 1:
        actions.remove("r")
    return actions

def get_reward(current, visited):
    global cells
    if current == cells["goal"]:
        return 100
    if current in cells["red"]:
        return -20
    if current in cells["white"]:
        return -2
    if current in visited:
        return -2

def best_next_move(current):
    global Qvals
    r= current[0]
    c=current[1]
    moves=next_moves(current)
    maxq = -1000000
    for move in moves:
        if Qvals[r][c][move] > maxq:
            maxq = Qvals[r][c][move]
            allmax=[move]
        if Qvals[r][c][move] == maxq:
            allmax.append(move)
    ind = random.randrange(len(allmax))
    return allmax[ind]


def random_next_move(current):
    moves = next_moves(current)
    index = random.randrange(len(moves))
    return moves[index]

def random_or_best(current):
    global p
    r = random.uniform(0, 1)
    if r <= p:
        return random_next_move(current)
    if r >p:
        return best_next_move(current)

def perform_act(current, action):
    if action == "l":
        return (current[0], current[1] - 1)
    elif action == "r":
        return (current[0], current[1] + 1)
    elif action == "u":
        return (current[0] - 1, current[1])
    elif action == "d":
        return (current[0] + 1, current[1])

""" **************************************************** Learning phase **************************************************** """
epochs=3000
p=0.3
max_num_moves = 300
gamma = 0.9
alpha = 0.2
beta = 1
rewards=[]
average_rewards = []
last_rewards = []
regrets = []
for epoch in range(epochs):
    print(epoch)
    current_cell = cells["start"]
    current_move = random_or_best(current_cell)
    visited =[]

    for step in range(max_num_moves):
        if current_cell not in visited:
            visited.append(current_cell)

        next_cell = perform_act(current_cell, current_move)
        if next_cell == cells["goal"]:
            print("found")
            visited.append(next_cell)
            break
        next_move = random_or_best(next_cell)
        reward = get_reward(next_cell, visited)
        rewards.append(reward)

        Qvals[current_cell[0]][current_cell[1]][current_move] = ( (1 - alpha) * Qvals[current_cell[0]][current_cell[1]][current_move] ) + ( alpha * (reward + gamma * Qvals[next_cell[0]][next_cell[1]][next_move]) )
        current_cell= next_cell
        current_move = next_move

    avg = sum(rewards) / len(rewards)
    last_rewards.append(reward)
    average_rewards.append(avg)
    regrets.append(max(average_rewards) - avg)
    p = p * 0.95
    beta = beta * 1.01

print(visited)
"""**************************************************************************************************************************"""
print(Qvals)


""" *********************************************** Ploting the optimum path ************************************************ """

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
Blue=(0, 0, 255)
Pcolor=(200,100,185)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
# This sets the margin between each cell
MARGIN = 2
grid = []
for row in range(Row):
    grid.append([])
    for column in range(Column):
        grid[row].append(0)  # Append a cell
grid=final_path
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIDTH*Column + (Column+1)*MARGIN,HEIGHT*Row + (Row+1)*MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("MAZE")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 15)
# -------- Main Program Loop -----------
current_cell = cells["start"]
for step in visited:
    final_path[step[0]][step[1]]="1"
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            break  # Flag that we are done so we exit this loop
    # Set the screen background
    screen.fill(BLACK)
    # Draw the grid
    for row in range(Row):
        for column in range(Column):
            color = WHITE
            if grid[row][column] == str(0):
                color = WHITE
            if grid[row][column] == str(1):
                color = GREEN
            if grid[row][column] == str(2):
                color = RED
            if grid[row][column] == str(3):
                color = Blue
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    # Limit to 60 frames per second
    clock.tick(30)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    time.sleep(0.1)

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
pygame.quit()



"""**************************************************************************************************************************"""







print(average_rewards)
episodes = range(epochs)
plt.plot(episodes, average_rewards)

plt.title('Average reward for p =0.3')
plt.xlabel('episode')
plt.ylabel('average reward')
plt.show()

plt.plot(episodes, regrets)
plt.title('Regret for p =0.3')
plt.xlabel('episode')
plt.ylabel('regret')
plt.show()







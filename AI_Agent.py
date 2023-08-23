import numpy as np
from MultiCheck import *
from aiPrep import *

ACTIONS = { 0:'Fold',
            1:'Call/Check', 
            2:'Bet/Raise_Small', 
            3:'Bet/Raise_Med',
            4:'Bet/Raise_Big', 
            5:'AllIn'}


class Agent(object):
    handHist = []
    def __init__(self, states, alpha = 0.15, random_factor=0.2):
        self.state_history = [(0,0,0)]
        self.alpha = alpha
        self.random_factor = random_factor

        self.G = {}
        self.init_reward(states)

    def init_reward(self,states):
        for i in range(len(states)):
            greedyArr = []
            for _ in range(6):
                greedyArr.append(np.random.uniform(high=1.0, low = 0.1))
            self.G[i] = greedyArr

    def update_state_history(self,reward):
        for state, next_move in self.handHist:
            self.state_history.append((state,next_move,reward))
        handHist = []

    def step(self, outcome):
        reward= 0
        if outcome == 0:
            reward = -1
        if outcome == 1:
            reward = -0.5   
        if outcome == 2:
            reward = 0.5   
        if outcome == 3:
            reward = 1

        return reward

    
    def learn(self,outcome):
        a = self.alpha
        target = self.step(outcome)
        self.update_state_history(target)

        for state, next_move, reward in self.state_history:
            self.G[2*state][next_move] = self.G[2*state][next_move] + a*(target-self.G[2*state][next_move])

        self.state_history = []
        self.random_factor -= 10e-5

    def choose_action(self, state, allowed_moves):
        n = np.random.random()
        if n<self.random_factor:
            next_move = np.random.choice(allowed_moves)
        else:
            maxG = -10e-15
            next_move = self.G[2*state].index(max(self.G[2*state]))
            if self.G[2*state][next_move] < maxG:
                next_move = 0              
        self.handHist.append((state,next_move))
        return next_move
    

def Init_AI_Agent(): 
    arr = []
    for x in range(1,2652):
        arr.append(x/2)
    ai_agent = Agent(arr, alpha = 0.1, random_factor=0.25)
    return ai_agent

def ai_decision(ai_agent, hand, board, pot, betVal, stack, absVal):
    action = ai_agent.choose_action(absVal, [0,1,2,3,4,5])

    if action == 0:
        if betVal == 0:
            bet = 'Check'
        else:
            bet = 'Fold'
        betSize = 0
    elif action == 1:
        betSize = betVal
        if betVal == 0:
            bet = 'Check'
        else:
            bet = 'Call'
    elif action == 2:
        betSize = round(0.3*(pot+betVal) + 2*betVal)
        bet = 'Raise'
    elif action == 3:
        betSize = round(0.75*(pot+betVal) + 2*betVal)
        bet = 'Raise'
    elif action == 4:
        betSize = round(1.25*(pot+betVal) + 2*betVal)
        bet = 'Raise'
    elif action == 5:
        betSize = stack
        bet = 'AllIn'

    return bet, betSize

def findAbsVal(absVal, hand):
    i = 0
    while (absVal[i][0][0] != hand[0] and absVal[i][0][1] != hand[1]) and (absVal[i][0][0] != hand[1] and absVal[i][0][1] != hand[0]):
        i+=1
    return i
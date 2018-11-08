# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 08:02:22 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import gym

#make env
env = gym.make('CartPole-v0')

#Print out possible actions/observation 
print(env.action_space)
print(env.observation_space)

#Defualt env
observation = env.reset()

for t in range(1000):
    env.render()
    cartPos, cartVel, poleAng, angVel = observation #Get what observation returns
    
    #Learning agent logic
    #Hard coded policy
    if poleAng > 0: #Lean to right
        action = 1
    else:           #Lean to left
        action = 0
      
    #Feed learned action into step function
    observation, reward, done, info = env.step(action)
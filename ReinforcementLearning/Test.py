# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 07:43:10 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import gym

#Create environment
env = gym.make('CartPole-v0')

#Reset to starting point
print("Initial Observation")
observation = env.reset()
print(observation) #Show env state

#Time steps
for _ in range(2):
    
    #env.render() #View env
    
    #Take random action of possible actions avaliable
    action = env.action_space.sample()
    #Get the 4 return 
    observation, reward, done, info = env.step(action)
    
    print("Preformed Action")
    print('\n')
    print("Observation")
    print(observation)
    print('\n')
    print("Reward")
    print(reward)
    print('\n')
    print("Done")
    print(done)
    print('\n')
    print("Info")
    print(info)
    print('\n')
    
    



# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:04:52 2018

@author: Matthew
Markov Model
"""
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

#method get Markov Edges
#This maps transitions probability dataframe
#to markov edges and weights
def getMarkovEdges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] = Q.loc[idx,col]
    return edges

#Create state space and initial state probabilities

state = ['Running' , 'Jumping', 'Eating'] #States
prob = [0.35, 0.35, 0.3] #Initial probabilities

state_space = pd.Series(prob, index = state, name = 'State')
print('State Space')
print(state_space)

#Define transition probabilities i.e. the prob that it will stay in the same state
#or more to a differt state

#Matrix size is MxM where M is the number of states
q_df = pd.DataFrame(columns = state, index=state)
q_df.loc[state[0]] = [0.4, 0.2, 0.4]
q_df.loc[state[1]] = [0.44, 0.45, 0.1]
q_df.loc[state[2]] = [0.45, 0.25, 0.3]

print('State Matrix')
print(q_df)

#Create the edges for the Markov model
myEdges = getMarkovEdges(q_df)
print("Markov Edges")
print(myEdges)

#Vizulization
#Graph object
markovGraph = nx.MultiDiGraph()
#add nodes that represent states
markovGraph.add_nodes_from(state)
print(f'Nodes:\n{markovGraph.nodes()}\n')

#Use Edges to represent transittion probabilities
for k, v in myEdges.items():
    tmp_origin, tmp_destination = k[0], k[1]
    markovGraph.add_edge(tmp_origin, tmp_destination, weight=v, lable =v)
print(f'Edges:')
pprint(markovGraph.edges(data=True))

nx.draw_networkx(markovGraph)

#Hidden Markov Model example
#Create the state spacce and initial prob
hidden_state = ['Hungry','Full']
hProb = [0.5, 0.5] # Equal probability for each hidden state

#Creat Hiddent transition matrix
#alpha
#Matrix size is MxM
a_df = pd.DataFrame(columns= hidden_state, index = hidden_state)
a_df.loc[hidden_state[0]] = [0.7, 0.3]
a_df.loc[hidden_state[1]] = [0.4, 0.6]

print('Hidden States')
print(a_df)

alpha = a_df.values

#Create matrix of observation probabilities
#Beta is the observation prob given a state
#O is number of differnt possible observations
#Matrix size is MxO

observable_state = state

b_df = pd.DataFrame(columns = observable_state, index=hidden_state)
b_df.loc[hidden_state[0]] = [0.2, 0.6, 0.2]
b_df.loc[hidden_state[1]] = [0.4, 0.1, 0.5]

print('BETA Observable states')
print(b_df)

#Create graph edges and weights

hideEdgesWeight = getMarkovEdges(a_df)
pprint(hideEdgesWeight)

emitEdgesWeight = getMarkovEdges(b_df)
pprint(emitEdgesWeight)

#Graph hidden layers
hiddenGraph = nx.MultiDiGraph()
hiddenGraph.add_nodes_from(hidden_state)
print(f'Nodes:\n{hiddenGraph.nodes()}\n')

#edges are the hidden probabilities
for k, v in hideEdgesWeight.items():
    tmp_origin, tmp_destination = k[0], k[1]
    hiddenGraph.add_edge(tmp_origin, tmp_destination, weight = v, label = v)
    
#Edges for emission probabilites
for k, v in emitEdgesWeight.items():
    tmp_origin, tmp_destination = k[0], k[1]
    hiddenGraph.add_edge(tmp_origin, tmp_destination, weight = v, label = v)
    
print(f'Edges:')
pprint(hiddenGraph.edges(data=True))

print('Creating Graphs')
nx.draw_networkx(hiddenGraph)
    

    






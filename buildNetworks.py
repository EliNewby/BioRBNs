# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 17:28:04 2023

@author: Eli
"""

import networkx as nx
import numpy as np
from scipy import special as sp

"""
Function to build a network using the configuration model with a power law tail out-degree and a Poisson in-degree
Inputs:
    numNodes: Number of nodes in the built network
    negativeProbability: Probability that an edge in the network will be a negative edge
    seed: Random seed for the random number generator
    power: Power of the power law
    powerLawStart:  Degree where the power law tail begins.
                    ALl degrees less than powerLawStart have a uniform probability of 1/powerLawStart**power.
                    That is, the out-degree probabilty distribution is continuous, step-wise function that begins uniform and becomes a decreasing power law
    isStronglyConnected: If true, after generating the network, all non-strongly connected nodes are removed.
                         Note: If this is true, the returned graph will not necessarily have numNodes nodes because some will be removed.

Output:
    Returns a networkx DiGraph
"""

def buildNetwork(numNodes, negativeProbability=0.25, seed=0, power=3, powerLawStart=2,isStronglyConnected=True):
    rng = np.random.default_rng(seed)
    normSubtract = 0
    for i in range(1,powerLawStart):
        normSubtract+=1/i**power
    norm = sp.zeta(power)-normSubtract+(powerLawStart-1)/powerLawStart**power
    ks = []
    for _ in range(numNodes):
        rand = rng.random()
        k = 0
        val = 0
        while(val < rand):
            k+=1
            if(k < powerLawStart):
                val += 1/(powerLawStart**power*norm)
            else:
                val += 1/(k**power*norm)
            
            #val += A/k**3
        ks.append(k)
    
    G = nx.DiGraph()
    while(not (np.zeros(numNodes) == ks).all()):
        source, sink = rng.integers(0,numNodes,2)
        isNeg = rng.random() <= negativeProbability
        while(ks[source] == 0):
            source = rng.integers(0,numNodes)
        G.add_edge('n'+str(source), 'n'+str(sink), negative = isNeg)
        ks[source] = ks[source] - 1

    if(isStronglyConnected):               
        removedNodes = []
        largestSCC = max(nx.strongly_connected_components(G), key = len)
        for node in G.nodes():
            if(node not in largestSCC):
                removedNodes.append(node)
        G.remove_nodes_from(removedNodes)
        
    return G
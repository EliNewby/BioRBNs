# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:55:33 2023

@author: Eli
"""
import numpy as np
import pystablemotifs as sm
import os
import networkx as nx

"""
Function to write a nested canalyzing function for a node as a read-once function (RoF)
Inputs:
    G = Graph
    node = Node to generate rule for
    rng = Random number generator
    bias = Probability that the function output is 1
Output:
    String of nested canalyzing function for given node
"""
def generateNestedCanalyzingFunctionRoF(G, node, rng, bias = 0.5):
    inputs = [e[0] for e in G.in_edges(node)]
    negative = [G.get_edge_data(x, node)['negative'] for x in inputs]
    n = len(inputs)
    if(n == 0):
        rand = rng.random()
        val = 0
        if(rand < bias):
            val = 1
        return node + " *= " + str(val)
    order = list(rng.choice(inputs, n, replace = False))
    funct = str(node)+" *= "
    for i in range(len(order)):
        rand = rng.random()
        if(rand < bias):
            if(negative[inputs.index(order[i])]):
                funct += "not " + str(order[i]) + " and ("
            else:
                funct += str(order[i]) + " or ("
        else:
            if(negative[inputs.index(order[i])]):
                funct += "not " + str(order[i]) + " or ("
            else:
                funct += str(order[i]) + " and ("
    funct = funct[:-5].rstrip()
    funct += ")"*(len(inputs)-1)
    return funct

"""
Function to generate Boolean Nested Canalyzing Rule-sets for a given graph
Inputs:
    G = graph
    numRulesets = number of rule-sets to generate
    directoryPath = path to folder to save rule-sets in
                    if the given directory does not exist this function will create a new folder
                    this folder will be populated with numbered booleannet files for each rule-set
    fewestAtts = Fewest number of attractors that each rule-set must have
                 if this value is set to 0, every generated rule-set will be output without checking attractor number
    bias = Probability that the function output is 1
    seed = Random number generator seed
Output:
    Writes 'numRulesets' rulesets to 'directoryPath' directory in the Booleannet format
"""

def generateRulesets(G, numRulesets, directoryPath, fewestAtts = 1, bias = 0.5, seed = 0):
    numGood = 0
    rng = np.random.default_rng(seed)
    while(numGood < numRulesets):
        rules = ""
        for node in G.nodes():
            rules+=generateNestedCanalyzingFunctionRoF(G, node, rng)+'\n'
        if(fewestAtts == 0):
            writePath = directoryPath+'/NCFs_'+str(numGood)+'.booleannet'
            isExist = os.path.exists(directoryPath)
            if not isExist:
              os.makedirs(directoryPath)       
            f = open(writePath,'w')
            f.write(rules)
            f.close()
            numGood += 1
        else:
            primes = sm.format.create_primes(rules)
            max_simulate_size = 0
            ar = sm.AttractorRepertoire.from_primes(primes, max_simulate_size=max_simulate_size)
            if(ar.fewest_attractors > 1):
                writePath = directoryPath+'/ROFs_'+str(numGood)+'.booleannet'
                isExist = os.path.exists(directoryPath)
                if not isExist:
                  os.makedirs(directoryPath)       
                f = open(writePath,'w')
                f.write(rules)
                f.close()
                numGood += 1

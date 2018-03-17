#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 00:39:22 2018
@author: dumbPy
git    : https://github.com/dumbPy
"""

#Class locationNode is crated to be used as Node with Port Name and Timestamp
# a = locationNode('somePort', someTimestamp)) creates an instance of class locationNode
# the attributes of a can be accessed as a.location and a.timestamp
#Edge between these locationNode instances can be created as G.add_edge(a, b) for a, b as two instances
    
class locationNode(object):
    def __init__(self, location, timestamp):
        self.location = location
        self.timestamp = timestamp



# 1. Checks if the node exists alreay
# 2. If id does, returns it's LOCATION IN MEMORY 
#    as two exactly same instances of a class at different location are not same
# 3. If it doesn't, adds it and calls itself again for checking memory location of node and return it.
def add_node_if_required(G, locationNodeInstance):
    for node in list(G.nodes):
        if (node.location == locationNodeInstance.location 
        and node.timestamp == locationNodeInstance.timestamp):
            return node   
    node = G.add_node(locationNodeInstance)
    return add_node_if_required(G, locationNodeInstance)


"""
find_n_routes(Graph, source, destination) is a finction that finds 
max n routes between source and destination in a given Graph G
"""
#Tracks the number of routes found uptill now
n_routes = 0

def find_n_routes(G=None, source=None, destination=None, max_n_routes=1):
    if not G or not source:
        print("Insufficient Data Provided.. PLease make sure you provide Graph and Source")
        return([])
    if destination==None:
        destination=source
        
    def find_next_node(path_till_current_node):
        global n_routes
        if n_routes >= max_n_routes:    #To make sure loop ends when we find n routes
            return ([])
        #print(len(path_till_current_node))
        print(n_routes)
        
        #path_till_current_node is a list of all nodes from start till current_node
        current_node= path_till_current_node[-1]        
        neighbors = list(G.neighbors(current_node))
        
        # Condition 1, no neighbors
        if len(neighbors)==0:
            return([])
        
        # Condition 2, return chain ending with destination and other chains
        for node in neighbors:
            if node in path_till_current_node:
                neighbors.remove(node)
        for node in neighbors:
            if node.location == destination:
                destination_node = node
                neighbors.remove(destination_node)
                n_routes+=1
                return([path_till_current_node+[destination_node]]+[find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors])
        
        #No neighbor is destination, call recursively on all next nodes
        return([find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors])
    
    start_nodes = []
    for node in G.nodes():
        if node.location == source:
            start_nodes.append(node)
            print(node.location, node.timestamp)
    return ([find_next_node([start_node]) for start_node in start_nodes])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
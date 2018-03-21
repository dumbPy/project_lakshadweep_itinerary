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



# =============================================================================
# # 1. Checks if the node exists alreay
# # 2. If id does, returns it's LOCATION IN MEMORY 
# #    as two exactly same instances of a class at different location are not same
# # 3. If it doesn't, adds it and calls itself again for checking memory location of node and return it.
# =============================================================================
def add_node(G, locationNodeInstance):
    for node in list(G.nodes()):
        if (node.location == locationNodeInstance.location 
        and node.timestamp == locationNodeInstance.timestamp):
            return node   
    node = G.add_node(locationNodeInstance)
    return add_node(G, locationNodeInstance)


"""
find_n_routes(Graph, source, destination,max_n_routes) is a finction that finds 
max n routes between source and destination in a given Graph G
"""
#Tracks the number of routes found uptill now

n_routes = 0
def find_n_routes(G=None, source=None, destination=None, max_n_routes=None):
    """
    set max_n_routes=False for all possible routes
    """
    
    
    
    
    
    if max_n_routes==None:
        print('Set max_n_routes to False for all possible paths')
        return()
    if max_n_routes==False:
        max_n_routes=1
    
    routes = []
    
    
    
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
        #print(n_routes)
        
        #path_till_current_node is a list of all nodes from start till current_node
        current_node= path_till_current_node[-1]        
        neighbors = list(G.neighbors(current_node))
        
        # Condition 1, no neighbors
        if len(neighbors)==0 or n_routes>= max_n_routes:
            return()
        
        def filter_neighbors(neighbors):
            
            cleaned_neighbors = neighbors[:]
            #Cleaning neighbors of all nodes that shouldn't be there.
            if len(path_till_current_node)>= 2:
                node1 = path_till_current_node[-2]
                node2 = path_till_current_node[-1]
                if node1.location==node2.location:
                    last_edge_type = 'stay'
                else:
                    last_edge_type = 'travel'
            else:
                last_edge_type = None
            for node in neighbors:
                if node in path_till_current_node:
                    cleaned_neighbors.remove(node)
                
                if node.location==current_node.location and last_edge_type=='stay':
                    cleaned_neighbors.remove(node)

                if node.location != current_node.location and last_edge_type == 'travel':
                    cleaned_neighbors.remove(node)
                    
# =============================================================================
#                     print('reaching here')
#                     print(node1.location, node2.location, node2.timestamp)
#                     print(node.location, node.timestamp)
# =============================================================================
            return(cleaned_neighbors, last_edge_type)
        
        neighbors, last_edge_type = filter_neighbors(neighbors)
        
        
# =============================================================================
#         if len(path_till_current_node)>=2:
#             print('last edge: ', path_till_current_node[-2].location, last_edge_type, path_till_current_node[-1].location )
#             print([neighbor.location for neighbor in cleaned_neighbors])
# =============================================================================
        
        # Condition 2, return chain ending with destination and other chains
        for node in neighbors:
            if node.location == destination:
                destination_node = node
                neighbors.remove(destination_node)
                if max_n_routes!=False:
                    n_routes+=1
                routes.append(path_till_current_node+[destination_node])
                [find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors]
        
        #No neighbor is destination, call recursively on all next nodes
        [find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors]

    start_nodes = []
    for node in G.nodes():
        if node.location == source:
            start_nodes.append(node)
            #print(node.location, node.timestamp)
    [find_next_node([start_node]) for start_node in start_nodes]
    return(routes)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
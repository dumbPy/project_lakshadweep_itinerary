#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 19:14:49 2018
@author: dumbPy
git    : https://github.com/dumbPy
"""

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
    if destination=None:
        destination=source
    
    def find_next_edge(G, path_uptill_now, current_pos, destination):
        neighbors = G.neighbors(current_pos)
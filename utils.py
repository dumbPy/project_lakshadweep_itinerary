#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 00:39:22 2018
@author: dumbPy
git    : https://github.com/dumbPy
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import numpy as np
#Class locationNode is crated to be used as Node with Port Name and Timestamp
# a = locationNode('somePort', someTimestamp)) creates an instance of class locationNode
# the attributes of a can be accessed as a.location and a.timestamp
#Edge between these locationNode instances can be created as G.add_edge(a, b) for a, b as two instances
    
class locationNode(object):
    def __init__(self, location, timestamp):
        self.location = location
        self.timestamp = timestamp
        self.coords = coords[location]
    def __str__(self):
        return ('%s %s'%(str(self.location), str(self.timestamp)))
    def __repr__(self): return self.__str__()
    def __hash__(self):
        return (hash((self.location, self.timestamp)))
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.location == other.location and
                self.timestamp == other.timestamp
                )

class itinerary(object):
    def __init__(self, list_of_nodes, list_of_edge_data=None):
        self.nodes = list_of_nodes
        self.len_nodes = len(self.nodes)
        self.itin = nx.DiGraph()
        for i, node in enumerate(self.nodes[:-1]):
            if list_of_edge_data:
                edgeTime = self.nodes[i+1].timestamp-self.nodes[i].timestamp
                self.itin.add_edge(self.nodes[i], self.nodes[i+1], ship=str(list(list_of_edge_data[i].values())[0])+' '+str(edgeTime))
                self.edgeData = list_of_edge_data
            else:
                self.itin.add_edge(self.nodes[i], self.nodes[i+1])
                self.edgeData = [[]]*self.len_nodes-1
        self.duration = self.nodes[-1].timestamp-self.nodes[0].timestamp
        self.duration_D = pd.to_timedelta([self.duration]).astype('timedelta64[D]')[0]
        self.duration_h = pd.to_timedelta([self.duration]).astype('timedelta64[h]')
    # def nodes(self):
    #     return (self.nodes)
    def __str__(self):
        for i, node in enumerate(self.nodes[:-1]):
            print(node.location, node.timestamp)
            print(self.itin.get_edge_data(self.nodes[i], self.nodes[i+1]), self.nodes[i+1].timestamp-self.nodes[i].timestamp)
        destination = self.nodes[-1]
        print(destination.location, destination.timestamp)
        print('Tour Duration: ', self.nodes[-1].timestamp-self.nodes[0].timestamp)
        return('')
    def draw(self, m:folium.Map=None, print_=False):
        if print_ : print(self)
        try:
            get_ipython # Throws error if running in Terminal. Works in jupyter notebook
            if m is None:
                m = folium.Map([10.99,73.66], zoom_start=7)
                # m.add_child(folium.LatLngPopup())
            print(len(self.nodes[:-1]))
            t_format = '%Y-%m-%d %I:%M %p'
            for i,node in enumerate(self.nodes[:-1]):
                if i%2==0: # Even Edges starting from 0th edge represent travel
                    folium.PolyLine(locations = self.curve(node.coords, self.nodes[i+1].coords),
                    popup=str(self.itin.get_edge_data(node, self.nodes[i+1])),
                    tooltip=f'{node.location} to {self.nodes[i+1].location}'
                    ).add_to(m)
                else: # Odd Edges starting from 1st edge represents stay
                    stay_end = self.nodes[i+1].timestamp
                    stay_start = self.nodes[i].timestamp
                    stay_time = stay_end-stay_start
                    popup_message = f'Stay From: {stay_start.strftime(t_format)} \
                                    Stay Till {stay_end.strftime(t_format)} Duration: {stay_time}'
                    folium.Marker(node.coords, popup=popup_message, tooltip=node.location).add_to(m)
            # Start and End nodes
            duration = self.nodes[-1].timestamp-self.nodes[0].timestamp
            if self.nodes[0].location==self.nodes[-1].location:
                message = f'Tour Start: {self.nodes[0].timestamp.strftime(t_format)}  \
                            Tour End: {self.nodes[-1].timestamp.strftime(t_format)} \
                            Duration: {duration}'
                folium.Marker(self.nodes[-1].coords, popup=message, tooltip=self.nodes[0].location).add_to(m)
            else: # Different Start and End Nodes
                folium.Marker(self.nodes[0].coords, popup=f'Start: {self.nodes[0].timestamp.strftime(t_format)} \
                    Duration: {duration}', tooltip=self.nodes[0].location).add_to(m)
                folium.Marker(self.nodes[-1].coords, popup=f'End: {self.nodes[-1].timestamp.strftime(t_format)} \
                    Duration: {duration}', tooltip=self.nodes[-1].location).add_to(m)
            return m
        except: 
            if not print_: print(self)
            print("Draw only works in Jupyter Notebook!!")

    @staticmethod
    def curve(start, end):
        center = [np.mean([start[0],end[0]]), np.mean([start[1],end[1]])]
        center[0]+=0.1*np.sign(end[0]-start[0])
        center[1]+=0.1*np.sign(end[1]-start[1])
        return [start, center, end]



#Tracks the number of routes found uptill now
n_routes = 0

def find_n_routes(G, source:'list of inland ports'=None, destination:'list of inland ports'=None, 
                    max_n_routes=np.infty, duration=None, **kwargs):
    """
    find_n_routes(Graph, source, destination,max_n_routes) is a function that finds 
    max n routes between source and destination in a given Graph G
    """ 
    # n_routes = 0
    inlandPorts = ['Kochi', 'Mangalore', 'Beypore']
    routes = []
    if source is None: source = inlandPorts
    if destination is None : destination = inlandPorts
        
    def find_next_node(path_till_current_node):
        global n_routes
        if n_routes >= max_n_routes:    #To make sure loop ends when we find n routes
            return ([])
        # path_till_current_node is a list of all nodes from start till current_node
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
                """Removing All unwanted neighboring nodes
                """
                if node in path_till_current_node:
                    cleaned_neighbors.remove(node)
                
                if node.location==current_node.location and last_edge_type=='stay':
                    cleaned_neighbors.remove(node)

                if node.location != current_node.location and last_edge_type == 'travel':
                    cleaned_neighbors.remove(node)
                    
            return(cleaned_neighbors, last_edge_type)
            
        neighbors, last_edge_type = filter_neighbors(neighbors)
        
        # Condition 2, return chain ending with destination and other chains
        for node in neighbors:
            if node.location in destination:
                destination_node = node
                neighbors.remove(destination_node)
                if max_n_routes!=False:
                    n_routes+=1
                nodeList = path_till_current_node+[destination_node]
                edgeDataList = [G.get_edge_data(nodeList[i], nodeList[i+1]) for i, node in enumerate(nodeList[:-1])]
                itinInstance = itinerary(nodeList, edgeDataList)
                if duration:
                    if itinInstance.duration_D<duration:
                        routes.append(itinInstance)
                else:
                    routes.append(itinInstance)
                [find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors]
        
        #No neighbor is destination, call recursively on all next nodes
        [find_next_node(path_till_current_node+[neighbor]) for neighbor in neighbors]

    start_nodes = []
    for node in G.nodes():
        if node.location in source:
            start_nodes.append(node)
            #print(node.location, node.timestamp)
    [find_next_node([start_node]) for start_node in start_nodes]
    global n_routes
    n_routes = 0
    return(routes)
        
        
coords = {
    'Kadmat':[11.2212,72.7754],
    'Agatti':[10.8679,72.1954],
    'Bitra' :[11.5981,72.1852],
    'Chetlat':[11.6938,72.7106],
    'Kiltan':[11.4886,73.0031],
    'Amini':[11.1269,72.7315],
    'Kavaratti':[10.5699,72.6378],
    'Kalpeni':[10.0706,73.6443],
    'Androth':[10.8171,73.6778],
    'Bangaram':[10.9397,72.2872],
    'Minicoy':[8.2740,73.0496],
    'Beypore':[11.1650,75.8028],
    'Kochi':[9.9692,76.2592],
    'Mangalore':[12.8514,74.8230]
}
        
        
        
        
        
        
        
        
        
        
        

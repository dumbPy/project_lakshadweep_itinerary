#!/usr/bin/env python3
"""
@author: dumbPy
git    : https://github.com/dumbPy
"""
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import folium
import numpy as np
from datetime import datetime
    
class locationNode:
    def __init__(self, location, timestamp, ship=None):
        self.location = location
        self.timestamp = timestamp
        self.ship = ship
        self.coords = coords[location]
    def __str__(self):
        return ('%s %s'%(str(self.location), str(self.timestamp)))
    def __repr__(self): return self.__str__()
    def __hash__(self):
        return (hash((self.location, self.timestamp, self.ship)))
    def __eq__(self, other):
        return (hash(self) == hash(other))
    
    @classmethod
    def fromRow(cls, row:pd.Series, filler=0, **kwargs):
        timestamp = row['Date']
        for col in row.keys()[1:]:
            if row[col]!= filler:
                location = row[col]
                ship = col
        return cls(location, timestamp, ship)


class Itinerary:
    def __init__(self, list_of_nodes, list_of_edge_data):
        self.nodes = list_of_nodes
        self.len_nodes = len(self.nodes)
        self.itin = nx.DiGraph()
        
        for i, node in enumerate(self.nodes[:-1]):
            edgeTime = self.nodes[i+1].timestamp-self.nodes[i].timestamp
            self.itin.add_edge(self.nodes[i], self.nodes[i+1], ship=str(list(list_of_edge_data[i].values())[0])+' '+str(edgeTime))
            self.edgeData = list_of_edge_data

    def __str__(self):
        for i, node in enumerate(self.nodes[:-1]):
            print(node.location, node.timestamp)
            print(self.itin.get_edge_data(self.nodes[i], self.nodes[i+1]), self.nodes[i+1].timestamp-self.nodes[i].timestamp)
        destination = self.nodes[-1]
        print(destination.location, destination.timestamp)
        print('Tour Duration: ', self.nodes[-1].timestamp-self.nodes[0].timestamp)
        return('')
    def __eq__(self, other):    return hash(self)==hash(other)
    def __hash__(self):         return hash(tuple(self.nodes))

    def draw(self, m:folium.Map=None, print_=False):
        if print_ : print(self)
        try:
            get_ipython # Throws error if running in Terminal. Works in jupyter notebook
            if m is None:
                m = folium.Map([10.99,73.66], zoom_start=7)
                # m.add_child(folium.LatLngPopup())
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

class RouteFinder:
    def __init__(self,G, source, destination, max_n_routes=np.infty,duration=None,**kwargs):
        self.G,self.source,self.destination,self.max_n_routes,self.duration = \
                G,source,destination,max_n_routes,duration
        start_nodes = [node for node in G.nodes if node.location in source]
        self.routes = []
        self.n_routes = 0 # counter for number of routes
        for node in start_nodes: self.walk([node])

    def addItinerary(self, nodes):
        edge_data = [self.G.edges[nodes[i], nodes[i+1]] for i in range(len(nodes)-1)]
        self.routes.append(Itinerary(nodes, edge_data))
    
    def walk(self, priv_path:list):
        """ Walk the next possible nodes.
        Return the list of previous walked nodes leading from source to destination
        """
        # End conditions for recursive loop
        current_node = priv_path[-1]
        if current_node.location in self.destination and len(priv_path)>1:
            self.addItinerary(priv_path)
            self.n_routes+=1
            return
        if self.n_routes >= self.max_n_routes:
            return

        if len(priv_path)>1:
            # Get metadata of last edge type
            last_edge = self.EdgeType(priv_path[-2], priv_path[-1])
        else: # If it's start of itinerary, next edge would be travel edge
              # So, make last edge as stay
              last_edge = 'stay'
        if last_edge == 'stay': # next edge will be travel i.e., ship not None
            next_nodes = [node for node in self.G.neighbors(current_node) 
                            if self.G.edges[current_node, node]['ship'] is not None]
        else: # Next edge will be stay, i.e., ship = None
            next_nodes = [node for node in self.G.neighbors(current_node)
                            if self.G.edges[current_node, node]['ship'] is None]
        
        for node in next_nodes:
            self.walk(priv_path+[node])

    def EdgeType(self, node1,node2):
        try:
            ship =  self.G.edges[node1, node2]['ship']
            if ship is None: return 'stay'
            else: return 'travel'
        except: raise ValueError(f'{node1} and {node2} have no edge between them')

    @staticmethod
    def find_routes(G, source:'list of inland ports'=None, destination:'list of inland ports'=None, 
                    max_n_routes=np.infty, duration=None, **kwargs):
        finder = RouteFinder(G=G, source=source, destination=destination, 
                    max_n_routes=max_n_routes, duration=duration, **kwargs)
        print('Total Routes Found: %i'%len(finder.routes))
        return finder.routes

   
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

#!/usr/bin/env python3
"""
@author: dumbPy <Sufiyan Adhikari>
git    : https://github.com/dumbPy
"""
"""
# =============================================================================
# This script is used to parse feasible itinerary for Lakshdweep
# Run `get_new_schedule.py` to download the schedule first
# =============================================================================
"""
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import utils, itertools
import matplotlib.pyplot as plt, numpy as np

#Used to neglect inland stay as a part of itinerary
inlandPorts = ['Kochi', 'Mangalore', 'Beypore']

# =============================================================================
# Variables Defined Below
# =============================================================================
params = {
'maxDaysOnOneIsland' : 5,
'duration' : 15, # Max duration of tour
'Departure' : datetime.strptime('11/03/2018', '%d/%m/%Y'), # Or use datetime.now()
'source' : inlandPorts,
'destination' : inlandPorts,
'minHoursOnOneIsland' : 3,
'maxHoursPerShip' : 24,
'max_n_routes' : np.infty,
'html_file' : 'Lakport_schedule.html',
'filler' : 0 # Used to fill NaN values
}
# =============================================================================
# Variables Defined Above
# =============================================================================


def parse_schedule(html_file:str, filler:int=0, **kwargs) -> pd.DataFrame:
    """function to parse ship schedule into `pandas.Dataframe`
    Input
    ------
    html_file:  path to html file from scraped from lakport.nic.in
    filler:     intiger to fill inplace of NAN values.

    Returns
    --------
    Schedule:   pandas.Dataframe of the schedule deduced from the `html_file`
    """
    df = pd.read_html(html_file, header = 0)[0]
    df['Date'] = pd.Series([datetime.strptime(time, '%d/%m/%Y') for time in df.loc[:, 'Date']])
    df.fillna(filler, inplace = True)
    df.set_index('Date', inplace=True)
    finalSchedule=[]
    for i,date in enumerate(df.index):
        for j, ship in enumerate(df.columns):
            if df.loc[date, ship] != filler:
                df.loc[date, ship] = '00:00'+df.loc[date, ship]
        for j, ship in enumerate(df.columns):
            if df.loc[date, ship] != filler:
                for l in range(len(df.loc[date, ship].split(" - ")) - 1):
                    dateAndTime = str(date)[:10]+' '+df.loc[date, ship].split(' - ')[l+1][:5]
                    #print(dateAndTime)
                    newRow = [datetime.strptime(dateAndTime, '%Y-%m-%d %H:%M')]+[filler]*len(df.columns)                
                    finalSchedule.append(newRow)
                    finalSchedule[-1][j+1] = df.loc[date, ship].split(' - ')[l][5:]
    finalSchedule.sort(key = lambda row:row[0]) # Sort by datetime
    finalSchedule = pd.DataFrame(finalSchedule, columns = ['Date']+list(df.columns))
    return finalSchedule


def check_conditions(   node1:utils.locationNode, node2:utils.locationNode, Departure, 
                        maxHoursPerShip, maxDaysOnOneIsland, minHoursOnOneIsland, other_G=None,**kwargs) -> ('bool','ship'):
    """Given 2 nodes and some parameters, check if the edge between them is possible
    """
 
    if  node1.timestamp > Departure and\
        node1.timestamp < node2.timestamp:
        
        # Stay Edge
        if      node1.location == node2.location and\
                node2.timestamp-node1.timestamp <= timedelta(days=maxDaysOnOneIsland) and\
                node2.timestamp-node1.timestamp >= timedelta(hours=minHoursOnOneIsland):
                if node1.location in inlandPorts: #Skip stay at mainland India
                        return False, None
                else:   return True, None # Else, consider stay edges at islands
        # Travel Edge
        elif    node1.ship == node2.ship and\
                (node2.timestamp-node1.timestamp) <= timedelta(hours=maxHoursPerShip):
                return True, node1.ship
        else:   return False, None
    else: return False, None


def generateGraph(cleaned_schedule, Departure, maxDaysOnOneIsland=5, 
                minHoursOnOneIsland=3, maxHoursPerShip=24, filler=0, **kwargs):
    G = nx.DiGraph()
    # Add all nodes to graph
    G.add_nodes_from([utils.locationNode.fromRow(row) for _,row in cleaned_schedule.iterrows()])
    print('Total Nodes Added: ', str(len(G.nodes)))
    for node1, node2 in itertools.permutations(list(G.nodes()), 2):
        cond, ship = check_conditions(node1, node2, 
                            Departure=Departure,
                            minHoursOnOneIsland=minHoursOnOneIsland,
                            maxHoursPerShip=maxHoursPerShip,
                            maxDaysOnOneIsland=maxDaysOnOneIsland)
        if cond: G.add_edge(node1, node2, ship = ship)
    print('Total Edges Added: ', str(len(G.edges)))
    return G

def get_all_routes(**params):
    cleanedSchedule = parse_schedule(**params)
    G = generateGraph(cleanedSchedule, **params)
    routes = utils.RouteFinder.find_routes(G, **params)
    return routes

if __name__=='__main__':
    cleanedSchedule = parse_schedule(**params)
    G = generateGraph(cleanedSchedule, **params)
    routes = utils.RouteFinder.find_routes(G, **params)
    for route in routes:
        print(route)
    print("Total Routes: %i"%len(routes))

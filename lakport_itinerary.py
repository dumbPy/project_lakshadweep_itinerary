#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 00:32:17 2018
@author: dumbPy
git    : https://github.com/dumbPy
"""
"""
# =============================================================================
# This script is used to parse feasible itinerary for Lakshdweep
# As the Ship Schedule page is captcha and text-selection protected,
# the schedule should be copied manually as follows.
# 
# VISIT http://lakport.nic.in/ship_online_programme.aspx
# SELECT 'All Passenger ships'. #here page will refresh is a fraction of sec.
# Enter the captcha but don't submit/click view yet.
# Right_click>Inspect>Network_Tab
# Now submit/click VIEW. #Some files will appear in Network Tab.
# Click 'ship_online_programme.aspx' and in that click Response sub-Tab.
# Copy the response into a txt file and import it below.
# =============================================================================
"""
import pandas as pd
from datetime import datetime
import networkx as nx
import numpy as np
import dumbpy_networkx_helper as dnh
import matplotlib.pyplot as plt


# =============================================================================
# Variables Defined Below
# =============================================================================

maxDaysOnOneIsland = 3
tourDuration = 15   #Not used in the code yet. for v2.0

Departure = datetime.strptime('11/03/2018', '%d/%m/%Y')
Start = 'Kochi'
End = 'Kochi'
minHoursOnOneIsland = 3
maxHoursPerShip = 30
max_n_routes = 20



#Used to neglect inland stay as a part of itinerary
inlandPorts = ['Kochi', 'Mangalore']

#url = os.path.expanduser("~/dropbox/projects/schedule_14_03_2018.html")  #use only if file is in some other directory
url = 'schedule_14_03_2018.html'
df = pd.read_html(url, header = 0)[0]
df['Date'] = pd.Series([datetime.strptime(time, '%d/%m/%Y') for time in df.loc[:, 'Date']])
filler = 0
df.fillna(filler, inplace = True)
actualSchedule = df.set_index('Date', inplace=True)

finalSchedule = [[Departure]+[Start]*len(df.columns)]
for i,date in enumerate(df.index):
    for j, ship in enumerate(df.columns):
        if df.loc[date, ship] != 0:
            df.loc[date, ship] = '00:00'+df.loc[date, ship]
    for j, ship in enumerate(df.columns):
        if df.loc[date, ship] != 0:
            for l in range(len(df.loc[date, ship].split(" - ")) - 1):
                dateAndTime = str(date)[:10]+' '+df.loc[date, ship].split(' - ')[l+1][:5]
                #print(dateAndTime)
                newRow = [datetime.strptime(dateAndTime, '%Y-%m-%d %H:%M')]+[0]*len(df.columns)                
                finalSchedule.append(newRow)
                finalSchedule[-1][j+1] = df.loc[date, ship].split(' - ')[l][5:]

finalSchedule = pd.DataFrame(finalSchedule, columns = ['Date']+list(df.columns))

#print([type(finalSchedule.loc[date, ship]) for date in finalSchedule.index for ship in finalSchedule.columns])


G = nx.MultiDiGraph()

temp_time = 0
temp_ship = 0
def setEdges():
    print('Calculating All Paths.. Please Wait')
    for (i, edgeStartDate) in zip(finalSchedule.index[finalSchedule.Date> Departure], finalSchedule.Date[finalSchedule.Date> Departure]):
        #print(edgeStartDate)
        global temp_time
        temp_time = edgeStartDate
        cond1 = list(finalSchedule.Date > edgeStartDate)
        cond2 = list((finalSchedule.Date-edgeStartDate).astype('timedelta64[D]') < maxDaysOnOneIsland)
        cond3 = list((finalSchedule.Date-edgeStartDate).astype('timedelta64[D]') >= 0)
        finalCond = [(a and b and c) for (a, b, c) in zip(cond1, cond2, cond3)]
        shortSchedule = finalSchedule[finalCond]
        #print(cond1, cond2, cond3, finalCond)
        #print(shortSchedule.shape)

        for j, edgeStartShip in enumerate(shortSchedule.columns[1:]):
            edgeStart = finalSchedule.loc[i, edgeStartShip]

            if edgeStart != filler:
                for iEnd, edgeEndDate in zip(shortSchedule.index, shortSchedule.Date):
                    for jEnd, edgeEndShip in zip(shortSchedule.index, shortSchedule.columns[1:]):
                        
                        edgeEnd = shortSchedule.loc[iEnd, edgeEndShip]
                        #if edgeEnd == edgeStart: #for only cross edges
                        if ((#Edge Indicating Island Stay, with min Hours on one island
                            (edgeEnd == edgeStart
                                  and pd.to_timedelta([edgeEndDate-edgeStartDate]).astype('timedelta64[h]')[0] > minHoursOnOneIsland) 
                            #Edge Indicating Travel, with max hrs on a single ship. (need to get down at island)
                            or (edgeEnd != 0 and edgeEndShip == edgeStartShip
                                  and pd.to_timedelta([edgeEndDate-edgeStartDate]).astype('timedelta64[h]')[0] < maxHoursPerShip))
                            #Neglect Edges between Ship Docking at Inland Port. Ship may Dock for a day or two at Inland Port.
                            and  not((edgeEnd in inlandPorts) and (edgeStart in inlandPorts))
                            ):
                            if edgeEnd != edgeStart: #edge representing travel
                                edgeShip = edgeStartShip
                            else:#Edge representing stay
                                edgeShip = None
                            edgeStartNode = dnh.add_node_if_required(G, dnh.locationNode(edgeStart, edgeStartDate))
                            edgeEndNode = dnh.add_node_if_required(G, dnh.locationNode(edgeEnd, edgeEndDate))
                            G.add_edge(edgeStartNode, edgeEndNode, ship = edgeShip)
                            #print(edgeStart,' - ', edgeEnd, '                  timing- ', [edgeStartDate, edgeEndDate],' ship= ', edgeShip)

setEdges()
routes = dnh.find_n_routes(G=G, source='Kochi', max_n_routes= max_n_routes)

def print_routes():
    
    for route in routes:
        for i, node in enumerate(route[:-1]):
            print(node.location, node.timestamp)
            print(G.get_edge_data(route[i], route[i+1])[0])
        destination = route[-1]
        print(destination.location, destination.timestamp)
        print()
print_routes()
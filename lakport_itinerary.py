"""
@author: dumbPy <Sufiyan Adhikari>
git    : https://github.com/dumbPy
"""
"""
# =============================================================================
# This script is used to parse feasible itinerary for Lakshdweep
# Run `get_new_schedule.py` to download the schedule first
# 
# Or, you may download the html page manually as follows.
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
import utils
import matplotlib.pyplot as plt, numpy as np

#Used to neglect inland stay as a part of itinerary
inlandPorts = ['Kochi', 'Mangalore', 'Beypore']

# =============================================================================
# Variables Defined Below
# =============================================================================
params = {
'maxDaysOnOneIsland' : 5,
'duration' : 15, # Max duration of tour
'Departure' : datetime.strptime('11/03/2018', '%d/%m/%Y'),
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




#print([type(finalSchedule.loc[date, ship]) for date in finalSchedule.index for ship in finalSchedule.columns])


def generateGraph(cleaned_schedule, Departure, maxDaysOnOneIsland=5, 
                minHoursOnOneIsland=3, maxHoursPerShip=24, filler=0, **kwargs):
    finalSchedule = cleaned_schedule
    # G initialized as Directional Graph. Nodes are set when setting Edges.
    G = nx.DiGraph()
    # temp_time = 0
    # temp_ship = 0

    print('Calculating All Paths.. Please Wait')
    for (i, edgeStartDate) in zip(finalSchedule.index[finalSchedule.Date> Departure],
                                  finalSchedule.Date[finalSchedule.Date> Departure]):
        #print(edgeStartDate)
        # global temp_time
        # temp_time = edgeStartDate
        cond1 = list(finalSchedule.Date > edgeStartDate)
        cond2 = list((finalSchedule.Date-edgeStartDate).astype('timedelta64[h]') <= maxDaysOnOneIsland*24)
        cond3 = list((finalSchedule.Date-edgeStartDate).astype('timedelta64[D]') >= 0)
        
        finalCond = [(a and b and c) for (a, b, c) in zip(cond1, cond2, cond3)]
        shortSchedule = finalSchedule[finalCond]
        
        for j, edgeStartShip in enumerate(shortSchedule.columns[1:]):
            edgeStart = finalSchedule.loc[i, edgeStartShip]

            if edgeStart != filler:
                for iEnd, edgeEndDate in zip(shortSchedule.index, shortSchedule.Date):
                    for jEnd, edgeEndShip in zip(shortSchedule.index, shortSchedule.columns[1:]):
                        
                        edgeEnd = shortSchedule.loc[iEnd, edgeEndShip]
                        #if edgeEnd == edgeStart: #for only cross edges
                        
# =============================================================================
#                      Conditions Needed to be satisfied by an Edge
# =============================================================================
                        # Edge Indicating Island Stay, with min Hours on one island
                        cond_a1 = (edgeEnd == edgeStart and 
                                  pd.to_timedelta([edgeEndDate-edgeStartDate]).astype('timedelta64[h]')[0] > minHoursOnOneIsland)
                        
                        # Edge Indicating Travel, with max hrs on a single ship. (need to get down at island)
                        cond_a2 = (edgeEnd != 0 and edgeEndShip == edgeStartShip
                                  and pd.to_timedelta([edgeEndDate-edgeStartDate]).astype('timedelta64[h]')[0] < maxHoursPerShip)
                            
                        # Neglect Edges between Ship Docking at Inland Port. Ship may Dock for a day or two at Inland Port.
                        cond_b = not((edgeEnd in inlandPorts) and (edgeStart in inlandPorts))
                        
                        if (( cond_a1 or cond_a2) and cond_b):
                            if edgeEnd != edgeStart: #edge representing travel
                                edgeShip = edgeStartShip
                            else:# Edge representing stay
                                edgeShip = None

                            # Creating Nodes
                            edgeStartNode = utils.locationNode(edgeStart, edgeStartDate)
                            edgeEndNode = utils.locationNode(edgeEnd, edgeEndDate)
                            # Adding Nodes and the connecting Edge to Graph
                            G.add_node(edgeStartNode); G.add_node(edgeEndNode)
                            G.add_edge(edgeStartNode, edgeEndNode, ship = edgeShip)
    return G

def get_all_routes(params):
    cleanedSchedule = parse_schedule(**params)
    G = generateGraph(cleanedSchedule, **params)
    routes = utils.find_n_routes(G=G, **params)
    return routes

if __name__=='__main__':
    cleanedSchedule = parse_schedule(**params)
    G = generateGraph(cleanedSchedule, **params)
    routes = utils.find_n_routes(G=G, **params)
    for route in routes:
        print(route)

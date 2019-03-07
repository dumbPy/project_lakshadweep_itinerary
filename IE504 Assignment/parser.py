import pandas as pd
from datetime import datetime


def parse_schedule(html_file:str, filler:int=0) -> pd.DataFrame:
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

    finalSchedule = pd.DataFrame(finalSchedule, columns = ['Date']+list(df.columns))
    return finalSchedule

if __name__ == '__main__':
    df=parse_schedule("Lakport_page.html", filler=0)
    print(df.head(n=10))

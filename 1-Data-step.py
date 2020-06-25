import pandas as pd
import numpy as np


def proc_pollData(SWING_STATES):
    '''
    Process 538 online polling data
        Args:
            SWING_STATES: list of swing states
        Returns: 
            Pandas DataFrame with results
    '''
    ### Load and filter data
    # dat = pd.read_csv("https://projects.fivethirtyeight.com/polls-page/president_polls.csv") 
    dat = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ56fySJKLL18Lipu1_i3ID9JE06voJEz2EXm6JW4Vh11zmndyTwejMavuNntzIWLY0RyhA1UsVEen0/pub?gid=0&single=true&output=csv")

    ### Keep swing states
    dat = dat[dat['state'].isin(SWING_STATES)]
    
    ### Get date
    dat = dat.assign(date = pd.to_datetime(dat['end.date'], format = "%m/%d/%Y"))

    ### Keep obs greater than 04/08/2020
    dat = dat[dat['date'] >= pd.to_datetime("2020-04-08")]
    
    ### Keep columns
    dat = dat[['date', 'state', 'biden', 'trump']]
    
    ### Rename Biden and Trump
    dat = dat.rename(columns={"biden": 'Biden', 'trump': 'Trump'})
    
    ### Reshape
    dat = dat.set_index(['date', 'state']).stack().reset_index()
        
    ### Rename columns
    dat.columns = ['date', 'state', 'candidate', 'pct']
    
    ### Convert pct to decimal 
    dat = dat.assign(pct = dat['pct']/100)
    
    return dat



if __name__ == "__main__":
    
    ### Constants
    # SWING_STATES = ["North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania",
    #                 "Texas", "Georgia", "Iowa", "Ohio", "Virginia", "Colorado"]

    SWING_STATES = ["NC", "MI", "AZ", "WI", "FL", "PA",
                    "TX", "GA", "IA", "OH", "VA", "CO"]
    
    CANDIDATE = ["Biden", "Trump"]


    ### Get and process The Economist polling data
    print("[1] Processing The Economist polling data")
    dat = proc_pollData(SWING_STATES)
    
    ### Save data
    print(f"[2] Saving: './data/processed_economist_polling_data.csv'")
    dat.to_csv('./data/processed_economist_data.csv', index=False)
    
    

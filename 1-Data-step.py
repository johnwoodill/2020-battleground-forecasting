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
    dat = pd.read_csv("https://projects.fivethirtyeight.com/polls-page/president_polls.csv") 

    ### Keep swing states
    dat = dat[dat['state'].isin(SWING_STATES)]
    
    ### Get date
    dat = dat.assign(date = pd.to_datetime(dat['end_date'], format = "%m/%d/%y"))

    ### Keep obs greater than 04/08/2020
    dat = dat[dat['date'] >= pd.to_datetime("2020-04-08")]
    
    ### Convert pct to decimal 
    dat = dat.assign(pct = dat['pct']/100)
    
    ### Get columns and rename
    dat = dat[['date', 'state', 'answer', 'pct']]
    dat = dat.rename(columns={'answer': 'candidate'})

    return dat



if __name__ == "__main__":
    
    ### Constants
    SWING_STATES = ["North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania",
                    "Texas", "Georgia", "Iowa", "Ohio", "Virginia", "Colorado"]
    CANDIDATE = ["Biden", "Trump"]


    ### Get and process 538 polling data
    print("[1] Processing 538 polling data")
    dat = proc_pollData(SWING_STATES)
    
    ### Save data
    print(f"[2] Saving: './data/processed_538_polling_data.csv'")
    dat.to_csv('./data/processed_538_polling_data.csv', index=False)
    
    

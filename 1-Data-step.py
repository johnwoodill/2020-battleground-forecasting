import pandas as pd
import numpy as np


def proc_pollData(swing_states):
    ### Load and filter data
    dat = pd.read_csv("https://projects.fivethirtyeight.com/polls-page/president_polls.csv") 

    ### Keep swing states
    dat = dat[dat['state'].isin(swing_states)]
    
    ### Get date
    dat.loc[:, 'date'] = pd.to_datetime(dat['end_date'], format = "%m/%d/%y")

    ### Keep obs greater than 04/08/2020
    dat = dat[dat['date'] >= pd.to_datetime("2020-04-08")]
    
    ### Recode candidate_name
    dat['candidate'] = dat['candidate_name'].replace("Joseph R. Biden Jr.", "Biden")
    dat['candidate'] = dat['candidate'].replace("Donald Trump", "Trump")
    
    ### Average daily polls
    dat = dat.groupby(['date', 'state', 'candidate'])['pct'].mean().reset_index()
    
    ### Convert pct to decimal 
    dat.loc[:, 'pct'] = dat['pct']/100

    return dat



if __name__ == "__main__":
    
    ### Constants
    SWING_STATES = ["North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania"]
    CANDIDATE = ["Biden", "Trump"]


    ### Get and process 538 polling data
    print("[1] Processing 538 polling data")
    dat = proc_pollData(SWING_STATES)
    
    ### Save data
    print(f"[2] Saving: './data/processed_538_polling_data.csv'")
    dat.to_csv('./data/processed_538_polling_data.csv', index=False)
    
    

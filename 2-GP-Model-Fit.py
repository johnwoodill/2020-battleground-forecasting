import pandas as pd 
import numpy as np
import pystan
import os
from datetime import date
import time


def proc_stan(c, s):
    ### Get c, s data
    dat_mod = dat[(dat['state'] == SWING_STATES[s]) & (dat['answer'] == CANDIDATE[c])]
     
    ### Get ndays from 2020-04-08
    dat_mod.loc[:, 'days'] = dat_mod.apply(lambda x: (pd.to_datetime(x['date']) - 
                                           pd.to_datetime("2020-04-08")).days, axis=1)
      
    ### Sort by days
    dat_mod = dat_mod.sort_values('days').reset_index(drop=True)
    
    ### Make stan data 
    
    stan_dat = dict(N = len(dat_mod), 
                    x = dat_mod['days'], 
                    y = dat_mod['pct'])
    
    ### Setup and fit stan model
    model = pystan.StanModel(file='gp.stan')            
    fit = model.sampling(data=stan_dat, 
                         iter=4000, 
                         chains=4)
                         
    # control=dict(adapt_delta=.9)    
    # WARNING:pystan:91 of 8000 iterations ended with a divergence (1.14 %).
    # WARNING:pystan:Try running with adapt_delta larger than 0.9 to remove the divergences.

    ### Get fitted values (can sample up to iterations)
    fv = fit.to_dataframe(pars='predicted_y', permuted=True).reset_index(drop=True)
    fv = fv[[col for col in fv if col.startswith('predicted_y')]]
    fv = fv.sample(100).reset_index(drop=True).reset_index()
    
    ### Build df and return
    fv.loc[:, 'state'] = SWING_STATES[s]
    fv.loc[:, 'candidate'] = CANDIDATE[c]
    
    return fv



if __name__ == "__main__":

    ### Constants
    SWING_STATES = ["North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania"]
    
    CANDIDATE = ["Biden", "Trump"]

    ### Get processed data
    print("[3] Reading: './data/processed_538_polling_data.csv'")
    dat = pd.read_csv('./data/processed_538_polling_data.csv')
    
    ### List compress results    
    print(f"[4] Processing Stan Model for: {SWING_STATES}")
    time.sleep(2)
    
    results = [proc_stan(c, s) for c in range(0, len(CANDIDATE)) for s in range(0, len(SWING_STATES))]
    
    ### -----------------------------
    #### INCOMPLETE ####
    # Need to bind results and save
    comp_results = []
    [comp_results.extend(el) for el in results]
    pd.concat([results[0], results[1])
    

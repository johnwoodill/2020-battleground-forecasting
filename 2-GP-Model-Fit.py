import pandas as pd 
import numpy as np
import pystan
import os
from datetime import date
import time


def proc_stan(c, s, dat):
    ### Get c, s data
    dat_mod = dat[(dat['state'] == SWING_STATES[s]) & (dat['candidate'] == CANDIDATE[c])]
     
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
    fv = fit.to_dataframe(pars='predicted_y').reset_index(drop=True)
    fv = fv[[col for col in fv if col.startswith('predicted_y')]]
        
    ### Order and rename predicted_y (rework)
    col_df = pd.DataFrame({'colnames': fv.columns})
    col_df['colnames'] = col_df['colnames'].str.extract('(\d+)')
    col_df['colnames'] = "pred_y" + col_df['colnames'].str.zfill(2)
    fv.columns = col_df['colnames'].astype(str).values
    fv = fv[sorted(fv.columns)]
    
    ### Change column names to date for ordering
    fv.columns = sorted(dat_mod['date'])
    
    ### Sample posterior
    fv = fv.sample(100).reset_index(drop=True)
    
    ### Build df and reshape from wide to long
    fv.insert(loc=0, column='candidate', value=CANDIDATE[c])
    fv.insert(loc=0, column='state', value=SWING_STATES[s])
    fv.insert(loc=0, column='sample', value=np.linspace(1, len(fv), len(fv)))
    
    outdat = pd.melt(fv, id_vars=['sample', 'state', 'candidate'], var_name='date', value_name='pct')
    
    return outdat



if __name__ == "__main__":

    ### Constants
    SWING_STATES = ["North Carolina", "Michigan", "Arizona", "Wisconsin", "Florida", "Pennsylvania"]
    CANDIDATE = ["Biden", "Trump"]

    ### Get processed data
    print("[3] Reading: './data/processed_538_polling_data.csv'")
    dat = pd.read_csv('./data/processed_538_polling_data.csv')
    
    ### List compress results    
    print(f"[4] Processing Stan Model for: {SWING_STATES}")
    time.sleep(2)   # Pause to show message before pystan output
    
    results = [proc_stan(c, s, dat) for c in range(0, len(CANDIDATE)) for s in range(0, len(SWING_STATES))]
    
    ### Bind all results and save
    bind_results = pd.concat([d for d in results])
    bind_results.to_csv("./data/model_results.csv", index=False)
    

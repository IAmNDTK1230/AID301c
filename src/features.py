from __future__ import annotations
import numpy as np
import pandas as pd

def make_features(df: pd.DataFrame, include_target: bool=True):
    x=df.copy(); dt=pd.to_datetime(x['date'])
    x['year']=dt.dt.year; x['month']=dt.dt.month; x['day']=dt.dt.day
    x['dayofyear']=dt.dt.dayofyear; x['dayofweek']=dt.dt.dayofweek
    x['ordinal']=dt.map(pd.Timestamp.toordinal)
    x['sin_doy']=np.sin(2*np.pi*x['dayofyear']/365.25); x['cos_doy']=np.cos(2*np.pi*x['dayofyear']/365.25)
    cols=['country','year','month','day','dayofyear','dayofweek','ordinal','sin_doy','cos_doy']
    return x[cols], x['revenue'] if include_target and 'revenue' in x else None

from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .config import DATA_RAW,DATA_PROCESSED
COUNTRIES=['United Kingdom','USA','Singapore','EIRE','Germany']

def _normalize_country(x):
    m={'united_states':'USA','united states':'USA','usa':'USA','singapore':'Singapore','united_kingdom':'United Kingdom','united kingdom':'United Kingdom','eire':'EIRE','germany':'Germany'}
    return m.get(str(x).strip().lower(),str(x).strip())

def load_json_transactions(raw_dir=DATA_RAW):
    rows=[]
    for p in sorted(Path(raw_dir).glob('*.json')):
        obj=json.loads(p.read_text(encoding='utf-8')); rows.extend([obj] if isinstance(obj,dict) else obj)
    return pd.json_normalize(rows) if rows else pd.DataFrame()

def build_sample_daily(days=500):
    rng=np.random.default_rng(42); dates=pd.date_range('2018-01-01',periods=days,freq='D')
    base={'United Kingdom':2400,'USA':1700,'Singapore':1200,'EIRE':1050,'Germany':950}; rows=[]
    for i,d in enumerate(dates):
        seasonal=1+.28*np.sin(2*np.pi*d.dayofyear/365.25)+(.30 if d.month in (11,12) else 0); trend=1+i*.0007
        for c in COUNTRIES:
            revenue=max(80,base[c]*seasonal*trend+rng.normal(0,base[c]*.10)); purchases=max(1,int(revenue/rng.uniform(35,55))); views=max(purchases,int(purchases*rng.uniform(8,18)))
            rows.append({'date':d.date().isoformat(),'country':c,'revenue':round(revenue,2),'purchases':purchases,'stream_views':views})
    return pd.DataFrame(rows)

def _coerce_transaction_schema(df):
    aliases={'invoice_date':'date','date':'date','country':'country','country_name':'country','price':'revenue','revenue':'revenue','total':'revenue','purchases':'purchases','stream_views':'stream_views','views':'stream_views'}
    df=df.rename(columns={c:aliases[c.lower()] for c in df.columns if c.lower() in aliases}).copy()
    if 'date' not in df or 'country' not in df: raise ValueError('Raw JSON data must include date/invoice_date and country/country_name fields')
    df['date']=pd.to_datetime(df['date'],errors='coerce'); df['country']=df['country'].map(_normalize_country)
    if 'revenue' not in df:
        qty=pd.to_numeric(df.get('quantity',1),errors='coerce'); unit=pd.to_numeric(df.get('unit_price',df.get('price',0)),errors='coerce'); df['revenue']=qty*unit
    if 'purchases' not in df: df['purchases']=1
    if 'stream_views' not in df: df['stream_views']=0
    df=df.dropna(subset=['date','country']); df['date']=df['date'].dt.date.astype(str)
    return df.groupby(['date','country'],as_index=False).agg(revenue=('revenue','sum'),purchases=('purchases','sum'),stream_views=('stream_views','sum'))

def ingest_data(raw_dir=DATA_RAW,output_path=None):
    output_path=Path(output_path or DATA_PROCESSED/'daily_revenue.csv'); output_path.parent.mkdir(parents=True,exist_ok=True)
    raw=load_json_transactions(raw_dir); daily=_coerce_transaction_schema(raw) if len(raw) else build_sample_daily()
    daily=daily.sort_values(['date','country']).reset_index(drop=True); daily.to_csv(output_path,index=False); return daily

if __name__=='__main__':
    d=ingest_data(); print(f'wrote {len(d):,} rows to {DATA_PROCESSED / "daily_revenue.csv"}')

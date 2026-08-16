import json,joblib,matplotlib.pyplot as plt,pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from .config import DATA_PROCESSED,MODEL_PATH,METRICS_PATH,ARTIFACTS
from .features import make_features
from .ingest import ingest_data
CAT=['country']; NUM=['year','month','day','dayofyear','dayofweek','ordinal','sin_doy','cos_doy']
def pipeline_for(model): return Pipeline([('prep',ColumnTransformer([('cat',OneHotEncoder(handle_unknown='ignore'),CAT),('num',StandardScaler(),NUM)])),('model',model)])
def time_split(df,frac=.8):
    dates=sorted(pd.to_datetime(df.date).unique()); cutoff=dates[int(len(dates)*frac)]; return df[pd.to_datetime(df.date)<cutoff],df[pd.to_datetime(df.date)>=cutoff]
def evaluate(model,train,test):
    Xtr,ytr=make_features(train); Xte,yte=make_features(test); model.fit(Xtr,ytr); pred=model.predict(Xte); return {'mae':float(mean_absolute_error(yte,pred)),'rmse':float(mean_squared_error(yte,pred)**.5)}
def train_and_compare(data_path=None,model_path=MODEL_PATH,metrics_path=METRICS_PATH):
    data_path=data_path or DATA_PROCESSED/'daily_revenue.csv'
    if not data_path.exists(): ingest_data(output_path=data_path)
    df=pd.read_csv(data_path); train,test=time_split(df)
    candidates={'baseline_mean':pipeline_for(DummyRegressor()),'linear_regression':pipeline_for(LinearRegression()),'random_forest':pipeline_for(RandomForestRegressor(n_estimators=120,max_depth=12,random_state=42,n_jobs=-1)),'gradient_boosting':pipeline_for(GradientBoostingRegressor(random_state=42,n_estimators=120,max_depth=3,learning_rate=.05))}
    results={n:evaluate(m,train,test) for n,m in candidates.items()}; best_name=min((k for k in results if k!='baseline_mean'),key=lambda k:results[k]['mae']); best=candidates[best_name]; X,y=make_features(df); best.fit(X,y)
    model_path.parent.mkdir(parents=True,exist_ok=True); joblib.dump(best,model_path); payload={'best_model':best_name,'models':results,'train_rows':len(train),'test_rows':len(test)}; metrics_path.parent.mkdir(parents=True,exist_ok=True); metrics_path.write_text(json.dumps(payload,indent=2))
    ARTIFACTS.mkdir(parents=True,exist_ok=True); fig,ax=plt.subplots(figsize=(8,4.5)); ax.bar(list(results),[results[n]['mae'] for n in results]); ax.set_ylabel('MAE'); ax.set_title('Model comparison vs baseline'); ax.tick_params(axis='x',rotation=20); fig.tight_layout(); fig.savefig(ARTIFACTS/'model_comparison.png'); plt.close(fig)
    eda=df.copy(); eda['date']=pd.to_datetime(eda.date); by=eda.groupby('country')['revenue'].sum().sort_values(ascending=False); fig,ax=plt.subplots(figsize=(8,4.5)); ax.bar(by.index,by.values); ax.set_title('Total revenue by country'); ax.tick_params(axis='x',rotation=25); fig.tight_layout(); fig.savefig(ARTIFACTS/'eda_revenue.png'); plt.close(fig); return payload
if __name__=='__main__': print(json.dumps(train_and_compare(),indent=2))

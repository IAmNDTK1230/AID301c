from pathlib import Path
import joblib,pandas as pd
from .config import MODEL_PATH
from .ingest import COUNTRIES
from .features import make_features

class RevenuePredictor:
    def __init__(self,model_path=MODEL_PATH): self.model_path=Path(model_path); self._model=None
    @property
    def model(self):
        if self._model is None: self._model=joblib.load(self.model_path)
        return self._model
    def predict(self,target_date,country=None):
        pd.Timestamp(target_date); countries=[country] if country else COUNTRIES
        X,_=make_features(pd.DataFrame({'date':[target_date]*len(countries),'country':countries}),False); vals=self.model.predict(X)
        items=[{'country':c,'prediction':round(float(v),2)} for c,v in zip(countries,vals)]
        return {'date':target_date,'predictions':items,'total_prediction':round(sum(x['prediction'] for x in items),2)}

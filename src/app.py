from __future__ import annotations
import time
try:
    from flask import Flask, jsonify, request
except ImportError:
    from .flask_compat import Flask, jsonify, request
from .config import MODEL_PATH
from .predict import RevenuePredictor
from .logging_service import log_prediction
from .monitor import monitoring_summary

def create_app(model_path=MODEL_PATH, log_path=None):
    app=Flask(__name__); predictor=RevenuePredictor(model_path)
    @app.get('/health')
    def health(): return jsonify({'status':'ok'})
    @app.route('/predict',methods=['GET','POST'])
    def predict():
        payload=request.get_json(silent=True) or request.args.to_dict()
        target_date=payload.get('date'); country=payload.get('country') or None
        if not target_date: return jsonify({'error':'date is required in YYYY-MM-DD format'}),400
        try:
            t=time.perf_counter(); result=predictor.predict(target_date,country); runtime=(time.perf_counter()-t)*1000
        except Exception as e: return jsonify({'error':str(e)}),400
        log_prediction({'date':target_date,'country':country},result,runtime,path=log_path)
        return jsonify(result)
    @app.get('/monitor')
    def monitor(): return jsonify(monitoring_summary(log_path))
    return app

app=create_app()
if __name__=='__main__': app.run(host='0.0.0.0',port=5000)

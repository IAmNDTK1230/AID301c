from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
DATA_RAW=ROOT/'data'/'raw'; DATA_PROCESSED=ROOT/'data'/'processed'; MODELS=ROOT/'models'; ARTIFACTS=ROOT/'artifacts'; LOGS=ROOT/'logs'
MODEL_PATH=Path(os.getenv('AAVAIL_MODEL_PATH',MODELS/'revenue_model.joblib'))
METRICS_PATH=Path(os.getenv('AAVAIL_METRICS_PATH',ARTIFACTS/'model_metrics.json'))
LOG_PATH=Path(os.getenv('AAVAIL_LOG_PATH',LOGS/'predictions.jsonl'))

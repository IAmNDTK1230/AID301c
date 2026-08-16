import json,time
from pathlib import Path
from .config import LOG_PATH

def log_prediction(payload,response,runtime_ms,path=None):
    path=Path(path or LOG_PATH); path.parent.mkdir(parents=True,exist_ok=True)
    record={'timestamp':time.time(),'request_type':'predict','input_data_summary':payload,'predictions':response,'runtime_ms':round(runtime_ms,3),'model_version':'1.0'}
    with path.open('a',encoding='utf-8') as f: f.write(json.dumps(record)+'\n')
    return record

def read_logs(path=None):
    path=Path(path or LOG_PATH)
    if not path.exists(): return []
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

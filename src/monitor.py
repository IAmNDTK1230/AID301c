import statistics
from .logging_service import read_logs

def monitoring_summary(log_path=None):
    logs=read_logs(log_path)
    if not logs: return {'requests':0,'avg_runtime_ms':None,'p95_runtime_ms':None}
    r=sorted(float(x.get('runtime_ms',0)) for x in logs); p95=r[min(len(r)-1,int(.95*(len(r)-1)))]
    return {'requests':len(logs),'avg_runtime_ms':round(statistics.mean(r),3),'p95_runtime_ms':round(p95,3)}

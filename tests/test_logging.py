from src.logging_service import log_prediction,read_logs
from src.monitor import monitoring_summary
def test_logging_is_isolated_from_production(tmp_path):
    p=tmp_path/'test_predictions.jsonl'; log_prediction({'date':'2020-01-01','country':'USA'},{'prediction':1},12.5,path=p); rows=read_logs(p); assert len(rows)==1 and rows[0]['runtime_ms']==12.5; s=monitoring_summary(p); assert s['requests']==1 and s['avg_runtime_ms']==12.5

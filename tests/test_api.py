from src.app import create_app
def test_health(trained_model,tmp_path): assert create_app(trained_model,tmp_path/'api.jsonl').test_client().get('/health').status_code==200
def test_predict_specific_country(trained_model,tmp_path):
    r=create_app(trained_model,tmp_path/'api.jsonl').test_client().post('/predict',json={'date':'2020-02-01','country':'USA'}); assert r.status_code==200 and r.get_json()['predictions'][0]['country']=='USA'
def test_predict_all_countries(trained_model,tmp_path):
    r=create_app(trained_model,tmp_path/'api.jsonl').test_client().get('/predict?date=2020-02-01'); assert r.status_code==200 and len(r.get_json()['predictions'])==5
def test_api_rejects_missing_date(trained_model,tmp_path): assert create_app(trained_model,tmp_path/'api.jsonl').test_client().post('/predict',json={'country':'USA'}).status_code==400

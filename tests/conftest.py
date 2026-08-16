import pytest
from src.ingest import ingest_data
from src.train import train_and_compare
@pytest.fixture(scope='session')
def trained_model(tmp_path_factory):
    d=tmp_path_factory.mktemp('capstone'); data=d/'daily.csv'; model=d/'model.joblib'; metrics=d/'metrics.json'; ingest_data(output_path=data); train_and_compare(data,model,metrics); return model

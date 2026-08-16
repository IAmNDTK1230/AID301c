from src.predict import RevenuePredictor
def test_model_predicts_specific_country(trained_model):
    r=RevenuePredictor(trained_model).predict('2020-01-15','Singapore'); assert len(r['predictions'])==1 and r['predictions'][0]['prediction']>0
def test_model_predicts_all_countries(trained_model):
    r=RevenuePredictor(trained_model).predict('2020-01-15'); assert len(r['predictions'])==5 and r['total_prediction']>0

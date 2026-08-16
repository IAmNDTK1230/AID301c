from src.ingest import ingest_data
def test_ingestion_is_automatable(tmp_path):
    out=tmp_path/'daily.csv'; df=ingest_data(output_path=out); assert out.exists() and len(df)>100; assert {'date','country','revenue','purchases','stream_views'}<=set(df.columns); assert df[['date','country','revenue']].isna().sum().sum()==0

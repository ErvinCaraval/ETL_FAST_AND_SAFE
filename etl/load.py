import pandas as pd
from pandas import DataFrame

def to_database(df, engine):
    df.to_sql('hechos_servicios', engine, if_exists='replace', index=False)

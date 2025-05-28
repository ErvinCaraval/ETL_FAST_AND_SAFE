import pandas as pd
import yaml
from sqlalchemy import create_engine
from etl import extract, transform, load

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

url_origen = f"postgresql://{config['CO_SA']['user']}:{config['CO_SA']['password']}@{config['CO_SA']['host']}:{config['CO_SA']['port']}/{config['CO_SA']['dbname']}"
engine_origen = create_engine(url_origen)

df = extract.get_data(engine_origen)
print(df.head())  # Ver primeras filas

import pandas as pd

def get_data(engine):
    query = "SELECT * FROM mensajeria_servicio"
    return pd.read_sql(query, engine)





import datetime
from datetime import timedelta, date, datetime
from typing import Tuple, Any
import numpy as np
import pandas as pd
from pandas import DataFrame



def clean_data(df):
    df['mes'] = df['fecha'].dt.month
    return df

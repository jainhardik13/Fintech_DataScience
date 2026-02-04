import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('financial_time_series.csv')

data.info()

# Convert date datatype to date time
data["date"] = pd.to_datetime(data["date"])
data.info()

# Daily total transaction amount
daily_total = data.set_index("date").resample("D")["amount"].sum()
print(daily_total)
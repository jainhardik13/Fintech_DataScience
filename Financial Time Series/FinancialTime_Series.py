import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.io.sas.sas_constants import platform_length

data = pd.read_csv('financial_time_series.csv')

data.info()

# Convert date datatype to date time
data["date"] = pd.to_datetime(data["date"], dayfirst=True)
data.info()


data.set_index("date", inplace=True)
# Daily total transaction amount
daily_total = data.resample("D")["amount"].sum()
print(daily_total.head())


# Weekly Average transaction amount
weekly_average = data.resample("W")["amount"].mean()
print(weekly_average.head())

# Monthly Average transaction amount
monthly_average = data.resample("ME")["amount"].mean()
print(monthly_average.head())

# Create readable week labels like "Jan Week 1"
weekly_df = weekly_average.reset_index()
weekly_df["Month"] = weekly_df["date"].dt.strftime("%b")
weekly_df["Week"] = ((weekly_df["date"].dt.day - 1)//7)+1

weekly_df["Week_label"] = (weekly_df["Month"] + " Week " + weekly_df["Week"].astype(str))

print(weekly_df[["Week_label", "amount"]])


# Monthly total transaction amount
monthly_total = data.resample("ME")["amount"].sum()
# Convert index to month name
monthly_df = monthly_total.reset_index()
# B for full name like JANUARY and b for jan
monthly_df["Month"] = monthly_df["date"].dt.strftime("%B")
print(monthly_df[["Month", "amount"]])

# Plot of Month with Total Amount using Seaborn
plt.figure(figsize = (8,6))
sns.barplot(x = monthly_df["Month"], y = monthly_df["amount"], palette = "Blues_d")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.show()

# Plot of month with total amount using matplot lib
plt.figure(figsize = (8,6))
plt.plot(monthly_df["Month"], monthly_df["amount"])
plt.title("Monthly total transaction amount")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.show()

# Weekly graph
plt.figure(figsize = (12,10))
plt.plot(weekly_df["Week_label"], weekly_df["amount"], marker = "o")
plt.title("Weekly average transaction")
plt.xticks(rotation = 90)
plt.xlabel("Week")
plt.ylabel("Amount")
plt.grid(True)
plt.show()

import numpy as np
import pandas as pd

# Load the data
# Validate the transactions
# Perform monthly and daily analysis
# Detect suspicious transactions
# Save results

# Importing the data and reading the file
data = pd.read_csv("bank_transactions.csv")

# print(data.head())
# data.info()

# Converting date into date time format
data["date"] = pd.to_datetime(data["date"])
data.info()

# Before analysis, we must ensure the data is logically correct
errors = []

if data["amount"].min() <= 0:
    errors.append("Invalid Transaction amount found")

if data.duplicated("transaction_id").any():
    errors.append("Duplicate transaction found")

if data["balance"].min() <= 0:
    errors.append("Negative balance found")


if errors:
    print("Data Validation Failed")

    for i in errors:
        print("-",i)
else:
    print("Data Validation Successful")

# Calculating total transaction amount per day D is for same date and combining the amount of transactions in that day
print("Daily average transaction amount: ")
daily_summary = data.set_index("date").resample("D")["amount"].sum()
print(daily_summary)


# Calculate the monthly summary transactions sum
print("Monthly average transaction amount: ")
monthly_summary = data.set_index("date").resample("ME")["amount"].sum()
print(monthly_summary)

# Detect Suspicious transactions
suspicious_transactions = data[data["amount"] > 8000]
# count of Suspicious Transactions
print(suspicious_transactions.shape)
# Other method of count Suspicious transactions
suspicious_transactions_count = len(suspicious_transactions)
print("Total suspicious transactions: ",suspicious_transactions_count)

suspicious_transactions.to_excel("Suspicious_transactions.xlsx", index=False)
# Importing the libraries
import numpy as np
import pandas as pd

data = pd.read_csv("Uncleaned.csv")

# Display the data
# print(data.head())
# Info about the data
# data.info()

# Number of rows and columns
# print(data.shape)

# calculating missing terms
# missing_count = data.isnull().sum()
# print(missing_count)

# Replacing a data in String format to numerical
data["Salary"] = data["Salary"].replace("Sixty Thousand", 60000)
# Changing the datatype of a column to numeric data
data["Salary"] = pd.to_numeric(data["Salary"])

# Python reads empty places as na and we are filling na places with average of te whole salary
data["Salary"] = data["Salary"].fillna(data["Salary"].mean())

# We are filling the age column which is below 18 and above 60 with nan and displaying the missing count
data.loc[(data["Age"]<18) | (data["Age"]>60), "Age"] = np.nan
missing_count = data.isnull().sum()
print(missing_count)

# Filling NA places in age with average of the age column
data["Age"] = data["Age"].fillna(data["Age"].mean())
missing_count = data.isnull().sum()
print(missing_count)

# print(data["Gender"].value_counts())

# Replacing not disclosed or unknown gender with others
# data["Gender"] = data["Gender"].replace("Not Disclosed","Others")
# data["Gender"] = data["Gender"].replace("Unknown", "Others")
# print(data["Gender"].value_counts())


# Standardize the gender column

valid_genders = ["Male", "Female"]
data["Gender"] = data["Gender"].apply(lambda i : i if i in valid_genders else "Others")
# print(data["Gender"].value_counts())

# print(data["Department"].value_counts())

data["Department"] = data["Department"].replace("Manegement","Management")
data["Department"] = data["Department"].replace("Sales&Marketing","Sales")

print(data["Department"].value_counts())

# Filling empty department value with the most repeating department
data["Department"] = data["Department"].fillna(data["Department"].mode()[0])
print(data["Department"].value_counts())
# data.info()

# Changing the datatype of date to dateTime
data["Hire Date"] = pd.to_datetime(data["Hire Date"], errors="coerce").fillna("Invalid Date")
data.info()

data["Age"] = data["Age"].astype(int)
data.info()
# print(data.head(20))

# modifying salary and filling the na places with salary average
data.loc[(data["Salary"]<20000) | (data["Salary"]>2000000), "Salary"] = np.nan
data["Salary"] = data["Salary"].fillna(data["Salary"].mean())

# Downloading the updated file
data.to_csv("cleaned.csv", index=False)
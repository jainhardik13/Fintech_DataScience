import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Haberman dataset
df = pd.read_csv('haberman.csv')

# Display basic information about the dataset
# print("Dataset Info:")
# print(df.head())
# print("\nDataset Shape:", df.shape)
# print("\nColumn Names:", df.columns.tolist())
# print("\nSurvival Status Distribution:")
# print(df['Survival_status'].value_counts())

print(df.head(20))
# Create Bar Plot visualization
plt.figure(figsize=(10, 6))

# 1. Survival Status Distribution (Bar Plot)
survival_counts = df['Survival_status'].value_counts()
print(survival_counts)

df["Survival_status"] = df["Survival_status"].map({1: "Survived", 2: "NotSurvived"})
print(df.head(20))

#stats
print(df.describe())

Survived_yes=df["Survival_status"]=="Survived"
print(Survived_yes)

Survived_no=df["Survival_status"]=="NOt Survived"
print(Survived_no)

print(Survived_yes.describe())
print(Survived_no.describe())

# plt.bar(['Survived', 'Not Survived'], survival_counts.values, color=["green", "yellow"])
# plt.title('Survival Status Distribution')
# plt.ylabel('Number of Patients')
# plt.xlabel('Status')
# # plt.grid(axis='y', alpha=0.3)

# Bar Graph of Survived and not Survived
plt.figure(figsize=(6, 4))
sns.countplot(x="Survival_status", data=df)
plt.title("Survived vs not survived")
plt.ylabel("No. of Patients")
plt.show()

# Histogram of patient age distribution
plt.figure(figsize=(8, 6))
sns.histplot(x="patient_age", data=df,bins=10)
plt.title("Patient age distribution")
plt.show()

# boxplot of Survival Status vs Age
plt.figure(figsize=(8, 6))
sns.boxplot(x="Survival_status", y="patient_age", data = df)
plt.title("Survival Status vs Age")
plt.show()

# Density plot of age distribution
plt.figure(figsize=(8, 6))
sns.kdeplot(x="patient_age", data = df)
plt.title("Age distribution")
plt.show()


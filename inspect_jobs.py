import pandas as pd

df = pd.read_csv("data/jobs/jobs.csv")
print("Rows and columns:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head(2).T)
import pandas as pd
df = pd.read_csv("C:\\Users\\Arpit0\\Downloads\\NEWO.csv")
df.interpolate(method='linear', inplace=True)
print(df)
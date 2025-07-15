import pandas as pd
df = pd.read_csv("src\data\zepto_products.csv")

print(df.head(5))
# print(df['timestamp'])
for elm in df.columns:
    print(elm)
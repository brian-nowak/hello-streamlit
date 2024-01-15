import pandas as pd
df = pd.read_csv("week1picks.csv")
df
# from prompt: turn first row of pandas dataframe into headers
# also drop a few unnecessary cols
# week1data.columns = week1data.iloc[0]
# week1data = week1data.drop(0)
# week1data = week1data.drop(['Timestamp', 'Best Bet', ''], axis=1)
# week1data
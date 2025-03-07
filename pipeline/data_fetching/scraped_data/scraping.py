import pandas as pd
import time

url = "https://en.wikipedia.org/wiki/National_Hockey_League#List_of_teams"
tables = pd.read_html(url)

df = tables[2][['Conference', 'Division', 'Team']]

#print(df[['Conference', 'Division', 'Team']].to_string)
print(df.__len__())
for i in range(df.__len__()):
    team = df.loc[i]
    print(f"division : {team["Division"]} team: {team["Team"]}")

    #print([['Conference', 'Division', 'Team']].to_string)
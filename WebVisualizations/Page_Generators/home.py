import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
import pandas as pd
import csv
import matplotlib.pyplot as plt
from scipy.stats import linregress



# source: https://data.world/datadavis/nba-salaries
players_df = pd.read_csv('../Resources/players.csv')
salaries_df = pd.read_csv('../Resources/salaries_1985to2018.csv')
players_df = players_df.rename(columns={"_id": "player_id"})
players_df.head()



career_salary_list = []
for player in salaries_df['player_id'].unique():
    this_player = salaries_df.loc[salaries_df["player_id"] == player, :]
    career_earnings = this_player['salary'].sum()
    player_salary_dict = {}
    player_salary_dict['player_id'] = player
    player_salary_dict['career_earnings'] = career_earnings
    career_salary_list.append(player_salary_dict)

   
nba_salary_df = pd.DataFrame(data=career_salary_list)

nba_df = pd.merge(players_df, nba_salary_df, on='player_id')
nba_df = nba_df.astype({'career_WS': 'float64', 'career_earnings': 'float64', 'draft_year': 'float64', 'career_PTS': 'float64'})

post_merger = pre_merger = nba_df.loc[nba_df["draft_year"] >= 1976, :]
eighties = post_merger.loc[post_merger["draft_year"] < 1990, :]
not_eighties = post_merger.loc[post_merger["draft_year"] >= 1990, :]
nineties = not_eighties.loc[not_eighties["draft_year"] < 2000, :]
not_nineties = not_eighties.loc[not_eighties["draft_year"] >= 2000, :]
aughts = not_nineties.loc[not_nineties["draft_year"] < 2010, :]
tens = not_nineties.loc[not_nineties["draft_year"] >= 2010, :]
pre_merger = nba_df.loc[nba_df["draft_year"] < 1976, :]

# post_merger['color']='black'
# eighties['color']='red'
# nineties['color']='purple'
# aughts['color']='blue'
# tens['color']='darkgreen'



nba_df = pd.DataFrame()
nba_df = pd.concat([nba_df, pre_merger])
nba_df = pd.concat([nba_df, eighties])
nba_df = pd.concat([nba_df, nineties])
nba_df = pd.concat([nba_df, aughts])
nba_df = pd.concat([nba_df, tens])

nba_df = nba_df.astype({'draft_year': 'float64'})


nba_df.rename(columns={'draft_year':'Draft Year',
                          'career_WS':'Career Win Shares',
                          'career_earnings':'Career Earnings',
                          'name': 'Name'}, 
                 inplace=True)
print(nba_df.columns)
import plotly.express as px

fig = px.scatter(nba_df, x="Career Win Shares", y="Career Earnings", color='Draft Year', title="Win Shares by Salary in NBA History",
                 hover_data=['Career Win Shares', 'Career Earnings', 'Name', 'Draft Year'], color_continuous_scale=px.colors.sequential.Jet)

fig.update_layout(
    title="Win Shares by Salary in NBA History",
    xaxis_title="Career Win Shares",
    yaxis_title="Career Earnings ($)",
    height=500,
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="Black"
    ),
    margin=dict(l=150, r=60, t=60, b=60),
    paper_bgcolor="LightSteelBlue",
)

fig.update_traces(marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
fig.show()

# fig = make_subplots(
#     rows=1, cols=1,
#     subplot_titles=("Pre-Merger", "1980s", "1990s", "2000s", "2010s"))

# fig.add_trace(go.Scatter(x=pre_merger['career_WS'], y=pre_merger['career_earnings'], fillcolor='black'),
#               row=1, col=1,)

# fig.add_trace(go.Scatter(x=eighties['career_WS'], y=eighties['career_earnings'], fillcolor='red'),
#               row=1, col=1,)

# fig.add_trace(go.Scatter(x=nineties['career_WS'], y=nineties['career_earnings'], color='purple'),
#               row=1, col=1,)

# fig.add_trace(go.Scatter(x=aughts['career_WS'], y=aughts['career_earnings'], fillcolor='blue'),
#               row=1, col=1,)

# fig.add_trace(go.Scatter(x=aughts['career_WS'], y=aughts['career_earnings'], fillcolor='darkgreen'),
#               row=1, col=1,)

# library(plotly)

# pal <- c("black", "red", "purple" , "blue" "darkgreen")
# pal <- setNames(pal, c("Pre-Merger", "1980s", "1990s", "2000s", "2010s"))

# p <- plot_ly(data = nba_df, x = nba_df['career_WS'], y = nba_df['career_earnings'], color = nba_df['color'], colors = pal)








plotly.offline.plot(fig, filename='../../index.html')
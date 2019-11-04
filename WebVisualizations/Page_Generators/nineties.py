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


fig = px.scatter(nineties, x=nineties['career_WS'], y=nineties['career_earnings'], hover_data=['name','draft_year'], height=400, trendline=True)

(slope, intercept, _, _, _) = linregress(nineties['career_WS'], nineties['career_earnings'])
fit = slope * nineties['career_WS'] + intercept

fig.add_trace(
    go.Scatter(x=nineties['career_WS'], y=fit,
    marker=go.Marker(color='purple'), name='Line of Best Fit'
))

fig.update_layout(
    title="Wins Shares by Salary (Drafted 1990-1999)",
    xaxis_title="Career Win Shares",
    yaxis_title="Career Earnings ($)",
    font=dict(
        family="Courier New, monospace",
        size=14,
        color="Black"
    ),
    margin=dict(l=150, r=60, t=60, b=60),
    paper_bgcolor="LightSteelBlue",
)

fig.update_traces(marker=dict(size=12, color='purple',
                              line=dict(width=2,
                                        color='DarkBlue')),
                  selector=dict(mode='markers'))
fig.show()



plotly.offline.plot(fig, filename='../Pages/nineties.html')
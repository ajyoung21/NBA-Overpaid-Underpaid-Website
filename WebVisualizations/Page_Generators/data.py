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

table = nba_df.to_html()


f = open('../Pages/data.html','w')

message = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8" />

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ" crossorigin="anonymous"></script>
    
     <link rel = "stylesheet"
       type = "text/css"
       href = "style.css" />
<title>Data</title>
</head>
<body>

        <a href="../../index.html" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="false">Home</a>

        <a href="analysis_overview.html" class="btn btn-outline-info" tabindex="-1" role="button" aria-disabled="false">Analysis Overview</a>

        <a href="pre_merger.html" class="btn btn-outline-dark" tabindex="-1" role="button" aria-disabled="false">Pre-Merger</a>

        <a href="eighties.html" class="btn btn-outline-danger" tabindex="-1" role="button" aria-disabled="false">1980s</a>

        <a href="nineties.html" class="btn btn-outline-secondary" tabindex="-1" role="button" aria-disabled="false">1990s</a>

        <a href="aughts.html" class="btn btn-outline-primary" tabindex="-1" role="button" aria-disabled="false">2000s</a>

        <a href="tens.html" class="btn btn-outline-success" tabindex="-1" role="button" aria-disabled="false">2010s</a>

        <a href="data.html" class="btn btn-outline-info" tabindex="-1" role="button" aria-disabled="false">Data</a>

      
      <p>{table}
  
    <div>
    </body>
</html>"""

f.write(message)
f.close()


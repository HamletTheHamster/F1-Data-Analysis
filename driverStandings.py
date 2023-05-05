import pandas as pd
import numpy as np
import plotly.express as px
from plotly.io import show
from plotly.io import kaleido as save
save.scope.default_scale = 5

from fastf1.ergast import Ergast

import datetime
import os
import sys

timestamp = datetime.datetime.now()

if len(sys.argv) > 0:
    note = sys.argv[1]

save = "Plots/" + timestamp.strftime("%Y-%b-%d") + "/" + timestamp.strftime("%X") + ": " + note + "/"
if not os.path.exists(save):
  os.makedirs(save)

ergast = Ergast()
races = ergast.get_race_schedule(2023)
results = []*5

# For each race in the season
for rnd, race in races['raceName'].items():

    if rnd < 4:
        # Get results. Note that we use the round no. + 1, because the round no.
        # starts from one (1) instead of zero (0)
        temp = ergast.get_race_results(season=2023, round=rnd + 1)
        temp = temp.content[0]

        # If there is a sprint, get the results as well
        sprint = ergast.get_sprint_results(season=2023, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
            # Add sprint points and race points to get the total
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        # Add round no. and grand prix name
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
        results.append(temp)
    else:
        temp = ergast.get_race_results(season=2023, round=1).content[0]
        temp['points'] = float('nan')
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'driverCode', 'points']]
        results.append(temp)


# Append all races into a single dataframe
results = pd.concat(results)
races = results['race'].drop_duplicates()

results = results.pivot(index='driverCode', columns='round', values='points')

# Rank the drivers by their total points
results['total_points'] = results.sum(axis=1)
results = results.sort_values(by='total_points', ascending=False)
results.drop(columns='total_points', inplace=True)

# Use race name, instead of round no., as column names
results.columns = races

pltTitle = "2023 Driver Standings"
fig = px.imshow(
    results,
    text_auto=True,
    aspect='auto',  # Automatically adjust the aspect ratio
    color_continuous_scale=[[0,    'rgb(198, 219, 239)'],  # Blue scale
                            [0.25, 'rgb(107, 174, 214)'],
                            [0.5,  'rgb(33,  113, 181)'],
                            [0.75, 'rgb(8,   81,  156)'],
                            [1,    'rgb(8,   48,  107)']],
    labels={'x': 'Race',
            'y': 'Driver',
            'color': 'Points'}       # Change hover texts
)
fig.update_xaxes(title_text='')      # Remove axis titles
fig.update_yaxes(title_text='')
fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                 showline=False,
                 tickson='boundaries')              # Show horizontal grid only
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                 showline=False, tickson='boundaries')    # And remove vertical grid
#fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')     # White background
fig.update_layout(coloraxis_showscale=False)        # Remove legend
fig.update_layout(xaxis=dict(side='top'))           # x-axis on top
fig.update_layout(
    title={
        'text': pltTitle,
        'font': dict(size=50),
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
#fig.update_layout(title_automargin=True)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=175))  # Remove border margins
#show(fig)

fig.write_image(save + pltTitle + ".pdf")
fig.write_image(save + pltTitle + ".png")

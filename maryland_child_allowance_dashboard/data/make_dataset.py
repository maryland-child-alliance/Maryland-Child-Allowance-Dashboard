import time
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask
from dash.exceptions import PreventUpdate
from dash import dash_table
import charts
import os
import json

import requests

# Import urlopen
from urllib.request import urlopen

df1 = pd.read_csv("summary.csv")
ov_pov_text = []
new_pov_text = []
pov_change_text = []
for ind in df1.index:
    ov_pov = df1["total_pov_rate"][ind]
    new_pov = df1["new_total_pov_rate"][ind]
    pov_change = df1["total_pov_change"][ind]

    ov_poverty = str(round(ov_pov * 100, 2)) + "%"
    new_poverty = str(round(new_pov * 100, 2)) + "%"
    poverty_change = str(pov_change) + "%"

    ov_pov_text.append(ov_poverty)
    new_pov_text.append(new_poverty)
    pov_change_text.append(poverty_change)

df1["total_pov_rate_%"] = ov_pov_text
df1["new_total_pov_rate_%"] = new_pov_text
df1["total_pov_change_%"] = pov_change_text
df1.to_csv("summary.csv", index=False)

from geojson_rewind import rewind


with open("districts_.json", "r") as openfile:
    # Reading from json file
    districts = json.load(openfile)

for k in range(len(districts["features"])):
    districts["features"][k]["properties"] = {"name": "{}".format(k + 1)}
    print(districts["features"][k]["properties"])


# print(len(districts['features']))
with open("districts_.json", "w") as outfile:
    json.dump(districts, outfile)

start = time.time()
response = requests.get(
    "https://raw.githubusercontent.com/fedderw/maryland-child-allowance/master/data/external/Maryland_Election_Boundaries_-_Maryland_Legislative_Districts_2012.geojson"
)
print(time.time() - start)
cts = response.json()
print(cts["features"][0])

with urlopen(
    "https://raw.githubusercontent.com/fedderw/maryland-child-allowance/master/data/external/Maryland_Election_Boundaries_-_Maryland_Legislative_Districts_2012.geojson"
) as response:
    print(response)
counties = json.load(response)

cts = counties["features"][0]
print(cts)

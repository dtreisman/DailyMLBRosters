# -*- coding: utf-8 -*-

# Quick Scraper to grab current roster of MLB players by team
# http://mlb.com/team_name_here/roster

# This script relies on the specific source code format of lines
# containing player names!

import requests
import pandas as pd
import numpy as np
from datetime import datetime

print("Pulling MLB Roster Data")
#Team codes

baseball = [
    'dbacks',
    'braves',
    'orioles',
    'redsox',
    'cubs',
    'whitesox',
    'reds',
    'guardians',
    'rockies',
    'tigers',
    'astros',
    'royals',
    'angels',
    'dodgers',
    'marlins',
    'brewers',
    'twins',
    'mets',
    'yankees',
    'athletics',
    'phillies',
    'pirates',
    'padres',
    'giants',
    'mariners',
    'cardinals',
    'rays',
    'rangers',
    'bluejays',
    'nationals']
# baseball = ["cardinals"]

pages = []
players = []
 


cols = ["team", "Date"]
for i in range(15):
    cols.append("pitcher_" + str(i + 1))
for i in range(5):
    cols.append("catcher_" + str(i+1))
for i in range(10):
    cols.append("infielder_" + str(i+1))
for i in range(10):
    cols.append("outfielder_" + str(i+1))
    
df_players = pd.DataFrame(columns = cols)

for team in baseball:
    r = requests.get("http://mlb.com/" + team + "/roster")
    pages.append(r.text)

for roster in pages:
    rost = []
    for line in roster.split("\n"):
        #print(line)
        if ">Pitchers<" in line:
            rost.append("Pitchers")
        if ">Catchers<" in line:
            rost.append("Catchers")
        if ">Infielders<" in line:
            rost.append("Infielders")
        if ">Outfielders" in line:
            rost.append("Outfielders")
        if "/player/" in line:
            ind = line.find('>')
            ind2 = line[ind:].find('<')
            rost.append(line[ind+1:(ind+ind2)])
    players.append(rost)
            
    df = pd.DataFrame(data = rost)
    # df = df.T
    # print(df)
    # df.columns = [team]
    # print(df)
    df["position"] = np.where(df[0] == "Pitchers", "pitcher", None)
    df["position"] = np.where(df[0] == "Catchers", "catcher", df["position"])
    df["position"] = np.where(df[0] == "Infielders", "infielder", df["position"])
    df["position"] = np.where(df[0] == "Outfielders", "outfielder", df["position"])
    df["position"] = df["position"].ffill()
    
    df_pitchers = df.loc[df["position"] == "pitcher"].drop("position", axis = 1)
    df_pitchers = df_pitchers.loc[df[0] != "Pitchers", ]
    df_pitchers = df_pitchers.T.reset_index(drop = "true")
    df_pitchers.columns = ["pitcher_" + str(x + 1) for x in range(df_pitchers.shape[1])]
    
    df_catchers = df.loc[df["position"] == "catcher"].drop("position", axis = 1)
    df_catchers = df_catchers.loc[df[0] != "Catchers", ]
    df_catchers = df_catchers.T.reset_index(drop = "true")
    df_catchers.columns = ["catcher_" + str(x + 1) for x in range(df_catchers.shape[1])]
    
    df_infielder = df.loc[df["position"] == "infielder"].drop("position", axis = 1)
    df_infielder = df_infielder.loc[df[0] != "Infielders", ]
    df_infielder = df_infielder.T.reset_index(drop = "true")
    df_infielder.columns = ["infielder_" + str(x + 1) for x in range(df_infielder.shape[1])]
    
    df_outfielder = df.loc[df["position"] == "outfielder"].drop("position", axis = 1)
    df_outfielder = df_outfielder.loc[df[0] != "Outfielders", ]
    df_outfielder = df_outfielder.T.reset_index(drop = "true")
    df_outfielder.columns = ["outfielder_" + str(x + 1) for x in range(df_outfielder.shape[1])]
    
    _df_players = pd.concat([df_pitchers, df_catchers, df_infielder, df_outfielder], axis = 1)
#     cols = []
#     for i in df_pitchers.columns:
#         if "index" not in i:
#             cols.append(i)
#     for i in df_catchers.columns:
#         if "index" not in i:
#             cols.append(i)
#     for i in df_infielder.columns:
#         if "index" not in i:
#             cols.append(i)
#     for i in df_outfielder.columns:
#         if "index" not in i:
#             cols.append(i)
# #     cols = [df_pitchers.columns, df_catchers.columns, df_infielder.columns, df_outfielder.columns] 
# #     cols[0] = "team"
#     __df_players.columns = cols

    df_players = pd.concat([df_players, _df_players], axis = 0)


#df.to_csv('players.csv', encoding='utf-8', index=False)

df_players["team"] = baseball
df_players = df_players.replace({"&#x27;":"'"}, regex = True)


# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
df_players["Date"] = dt_string

df_players = df_players.reset_index(drop = True)
# df_players.to_csv("DailyMLBRosters.csv", encoding='utf-8-sig', index=False)

old_data = pd.read_csv("data/DailyMLBRosters.csv", encoding='utf-8-sig')
new_data = pd.concat([old_data, df_players], axis = 0)
new_data.to_csv("data/DailyMLBRosters.csv", encoding='utf-8-sig', index=False)
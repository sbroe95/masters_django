import os
import sys
import json
from types import new_class
import pandas as pd
# from database.config import *
from datetime import datetime
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

DB_USER = config['DB_USER'] 
DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
DB_PASSWORD = config['DB_PASSWORD']

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine) 

os.system("sh update.sh")

cwd = os.getcwd()
print(cwd)

with open(f'{cwd}/data/data_new.json') as json_file:
    data = json.load(json_file)

players = data["players"]

image_dict = {}
with engine.connect() as con:
    rs = con.execute('SELECT * FROM player_images')
    for row in rs:
        image_dict[row[0]] = row[2]



for index, player in enumerate(players):
    if player["cut_element"]=="cut-score":
        cut_score = player["cut_score"]
        players.remove(player)

for player in players:

    if player["thru"]=="CUT":
        player["to_par"] = int(player["tot"])-140
    elif player["thru"]=="WD":
        player["to_par"]=1000
    elif player["to_par"]=="E":
        player["to_par"]=0
    else:
        player["to_par"] = int(player["to_par"])

    player.update(link=image_dict[player['player']])

    # player_link = player['link']
    # image_id = player_link.split('/')[-2]
    # new_link = f"https://a.espncdn.com/combiner/i?img=/i/headshots/golf/players/full/{image_id}.png&w=350&h=254"

    # # print(f"player : {player['player']}\n old link : {player_link}\n new link : {new_link}\n\n ")
    # player.update(link=new_link)


df = pd.DataFrame.from_records(players).drop(labels=["cut_score","cut_element"], axis="columns")
df['row_num'] = np.arange(len(df)) + 1

print(datetime.now())
print(f"{len(df['row_num'])} players data downloaded")

with Session() as session:
    session.execute("""DELETE FROM masters_espn WHERE 1=1""")
    df.to_sql('masters_espn', con=engine, if_exists='append',index=False)
    session.commit()
    session.close()


import os
import sys
import json
import pandas as pd
from database.config import *
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np

engine = create_engine(f'postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine) 

os.system("sh update.sh")

cwd = os.getcwd()
print(cwd)
# for root, dirs, other in os.walk(cwd):
#     print(f"root is {root}")
#     print(f"dirs is {dirs}")
#     print(f"other is {other}")

with open(f'{cwd}/data/data_new.json') as json_file:
    data = json.load(json_file)

players = data["players"]



name_mappings_dict = {
    # ESPN to common
    "Cam Davis": "Cameron Davis",
    "Matt Fitzpatrick": "Matthew Fitzpatrick",
    "K.H. Lee": "Kyoung-Hoon Lee",
    "Sung Kang":  "Sung-Hoon Kang",
    "Jacob Bridgeman (a)": "Jacob Bridgeman",
    "Dawie van der Walt":  "Dawie Van Der Walt",
    "Eugenio Chacarra (a)":  "Eugenio Lopez-Chacarra",
    "Greg Odom Jr. (a)":  "Gregory Odom Jr."
}



for index, player in enumerate(players):
    # print(index, player["player"])
    if player["cut_element"]=="cut-score":
        cut_score = player["cut_score"]
        players.remove(player)
        # print(f"cut score player{player['player']}")

for player in players:
    if player['player'] in name_mappings_dict:
        player['player'] = name_mappings_dict[player['player']]

    if player["thru"]=="CUT":
        # print("CUT")
        player["to_par"] = int(player["tot"])-144
    elif player["thru"]=="WD":
        player["to_par"]=1000
    elif player["to_par"]=="E":
        player["to_par"]=0
    else:
        player["to_par"] = int(player["to_par"])


df = pd.DataFrame.from_records(players).drop(labels=["cut_score","cut_element"], axis="columns")
df['row_num'] = np.arange(len(df)) + 1

print(datetime.now())
print(f"{len(df['row_num'])} players data downloaded")

with Session() as session:
    session.execute("""DELETE FROM masters_espn WHERE 1=1""")
    df.to_sql('masters_espn', con=engine, if_exists='append',index=False)
    session.commit()
    session.close()

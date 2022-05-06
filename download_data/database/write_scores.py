import psycopg2
import pandas as pd
import json
from config import *

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine) 

with open('data/data_new.json') as json_file:
    data = json.load(json_file)

players = data["players"]

for player in players:
    if player["cut_element"]=="cut-score":
        cut_score = player["cut_score"]
        players.remove(player)

df = pd.DataFrame.from_records(players).drop(labels=["cut_score","cut_element"], axis="columns")

print(df)

with Session() as session:
    session.execute("""DELETE FROM espn WHERE 1=1""")
    df.to_sql('espn', con=engine, if_exists='append',index=False)
    session.commit()


import psycopg2
import pandas as pd
import json
from config import *

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

engine = create_engine(f'postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine) 

dest_filename = "game.csv"
df = pd.read_csv(dest_filename).reset_index(drop=True)

print(df)

with Session() as session:
    session.execute("""DELETE FROM players WHERE 1=1""")
    df.to_sql('players', con=engine, if_exists='append',index=False)
    session.commit()
    session.close()


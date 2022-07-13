import json
import requests

from sqlalchemy import create_engine
#import pillow
from PIL import Image


with open('database/config.json') as config_file:
    config = json.load(config_file)

DB_USER = config['DB_USER'] 
DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
DB_PASSWORD = config['DB_PASSWORD']


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
with engine.connect() as con:
    rs = con.execute('SELECT * FROM player_images')
    image_dict = {}

    for row in rs:
        player_name_with_underscores = row[0].replace(" ", "_")
        if row[1] == 'default.jpg':
            image_filename = row[1]
        else:
            response = requests.get(row[1])
            
            player_name_with_underscores = row[0].replace(" ", "_")
            image_filename = f"{player_name_with_underscores}.jpg"

            if response.status_code==404:
                print(f"{row[0]} image not found")
                #Load the image
                img = Image.open('../media/default.jpg')
                img.save(f"../media/player_pics/{image_filename}")
                img.close()
            else:
                with open(f"../media/player_pics/{image_filename}", "wb") as file:
                    file.write(response.content)
                
        con.execute(f"UPDATE player_images SET image_name=\'{image_filename}\' WHERE player_name=\'{row[0]}\';")


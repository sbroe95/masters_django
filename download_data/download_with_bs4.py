from bs4 import BeautifulSoup
from numpy import number
import requests
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

def checkInt(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()


download_images_flag = True


url = "https://www.espn.com/golf/leaderboard"
page_html = requests.get(url).text
soup = BeautifulSoup(page_html, "html.parser")

records_list = []

for index, table_row in enumerate(
    soup.find_all("tr", {
        "class": "PlayerRow__Overview PlayerRow__Overview--expandable Table__TR Table__even"
    }
)):
    number_of_cells_in_row = len(table_row)
    if number_of_cells_in_row==3:
        player_dict = {} 
        link = table_row.find("a", {"class": "AnchorLink"})['href']
        player_name = table_row.find("a", {"class": "AnchorLink"}).text
        player_image_id = link.split('/')[7]
        # link = f"https://a.espncdn.com/combiner/i?img=/i/headshots/golf/players/full/{player_image_id}.png&w=350&h=254"

        player_name_with_underscores = player_name.replace(" ", "_")
        link = f"player_pics/{player_name_with_underscores}.jpg"
        if player_name == "Xander Schauffele":
            for item in table_row:
                print(f"\n{item}\n")
        cell_list = table_row.find_all("td")
        # print(cell_list)
        
        position = None
        country_flag_image = cell_list[1].find("img")['src']
        to_par = cell_list[2].text
        
        cut_flag = None
        to_par = 0
        today = None

        thru = cell_list[2].text
        r1 = None
        r2 = None
        r3 = None
        r4 = None
        tot = None
        row_num = index + 1

    elif len(table_row)==11:
        player_dict = {} 
        link = table_row.find("a", {"class": "AnchorLink"})['href']
        player_name = table_row.find("a", {"class": "AnchorLink"}).text
        player_image_id = link.split('/')[7]
        image_link = f"https://a.espncdn.com/combiner/i?img=/i/headshots/golf/players/full/{player_image_id}.png&w=350&h=254"

        player_name_with_underscores = player_name.replace(" ", "_")
        link = f"{player_name_with_underscores}.jpeg"
        
        
        cell_list = table_row.find_all("td")
        
        position = cell_list[1].text
        country_flag_image = cell_list[2].find("img")['src']
        to_par = cell_list[3].text
        
        cut_flag = None
        if checkInt(to_par):
            score = int(to_par)
        elif to_par == "E":
            score=0
        else:
            score = None
            cut_flag = to_par
        today = cell_list[4].text

        thru = cell_list[5].text
        r1 = cell_list[6].text
        r2 = cell_list[7].text
        r3 = cell_list[8].text
        r4 = cell_list[9].text
        tot = cell_list[10].text
        row_num = index + 1

    player_dict['pos'] = position
    player_dict['player'] = player_name
    player_dict['country_flag_image'] = country_flag_image
    player_dict['link'] = link
    player_dict['to_par'] = score
    player_dict['today'] = today
    player_dict['thru'] = thru
    player_dict['r1'] = r1
    player_dict['r2'] = r2
    player_dict['r3'] = r3
    player_dict['r4'] = r4
    player_dict['tot'] = tot
    player_dict['row_num'] = row_num

    # print(f"appending for index {index}, row {row_num}")
    records_list.append(player_dict)

df = pd.DataFrame.from_records(records_list)

print(df)


with open('database/config.json') as config_file:
    config = json.load(config_file)

DB_USER = config['DB_USER'] 
DB_HOST = config['DB_HOST']
DB_PORT = config['DB_PORT']
DB_NAME = config['DB_NAME']
DB_PASSWORD = config['DB_PASSWORD']

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
Session = sessionmaker(bind=engine) 

with Session() as session:
    session.execute("""DELETE FROM masters_espn WHERE 1=1""")
    df.to_sql('masters_espn', con=engine, if_exists='append',index=False)
    session.commit()
    session.close()

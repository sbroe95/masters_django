import requests
import pandas as pd
from bs4 import BeautifulSoup

def convert(s):
    try:
        return float(s)
    except ValueError:
        num, denom = s.split('/')
        converted = round(float(num) / float(denom))
        return converted

with open("paddy_power.html", "r", encoding='utf-8') as f:
    content= f.read()


soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify)

records_list = []

for item in soup.find_all("div", class_="grid outright-item"):
    name = item.contents[1].text.strip()
    odds = item.contents[3].text.strip()
    if name == "Rory McIlroy" and odds == "17/2":
        break
    odds = convert(odds)
    print(f"{name} : {odds}")

    records_list.append({"name":name, "odds": odds})


filename = "odds.csv"
df = pd.DataFrame.from_records(records_list)

df.to_csv(filename)

print("Done")
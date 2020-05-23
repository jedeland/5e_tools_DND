import random



import pandas as pd; import numpy as np; from bs4 import BeautifulSoup
import requests; import os; import re; import addon_pack_namegen
from pandas import json_normalize; import json
from unidecode import unidecode

def find_names():


    with open('xgtenames.json') as f:
        data = json.load(f)
    #print(data)
    titles = json_normalize(data, ["name"])
    #print(titles)
    catagories = json_normalize(data, ["name", "tables", "table"], max_level=1)
    #print(catagories, "\n\n\n", pd.unique(catagories.columns), "Yohooo")
    un_nested = json_normalize(data, ["name"], errors="ignore", meta_prefix="npc_", max_level=1)
    flatt_table_combines = pd.DataFrame()
    for i, r in un_nested.iterrows():
        json_string = r["tables"]
        #print(json.dumps(json_string))
        flatt_table = json_normalize(json_string, "table", ["option"])
        flatt_table["race"] = r["name"]
        #print(flatt_table)
        flatt = [flatt_table, flatt_table_combines]
        flatt_table_combines = pd.concat(flatt)
    print("\n\n\n", flatt_table_combines)
    df = flatt_table_combines
    df = df.drop(df[(df["race"] == "Gith")].index)
    df = df.loc[~(df["race"] == "Human")]
    print(pd.unique(df["race"]))
    print("\n\n\n", df)



    #Json data instead; https://github.com/TheGiddyLimit/TheGiddyLimit.github.io/blob/master/data/names.json - https://datatofish.com/load-json-pandas-dataframe/
    #Because of how the PDF is set out, the names need to be split - No longer using the PDF time for more webscraping !


find_names()
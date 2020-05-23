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
    df = df.drop(["min", "max"], 1)
    print(pd.unique(df["race"]))
    print("\n\n\n", df)
    return df
    #Json data instead; with written consent from TheGiddyLimit on 23/5/20
    #https://github.com/TheGiddyLimit/TheGiddyLimit.github.io/blob/master/data/names.json - https://datatofish.com/load-json-pandas-dataframe/
    #Because of how the PDF is set out, the names need to be split - No longer using the PDF time for more webscraping !

def create_names():
    df = find_names()
    #https://github.com/JKH4/name-generator using this as a basis for the name generator, thanks to JKH4
    #https://towardsdatascience.com/generating-pok%C3%A9mon-names-using-rnns-f41003143333
    print("Attempting to create new names using previous names")
    padd_start, padd_end = "#", "*"
    df["result"] = df["result"].map(lambda n: padd_start + n + padd_end)
    df = df.rename(columns={"result":"name"})
    df.describe()
    print('Example of names to be cleaned:')


    print('Max name size: {}'.format(df['name'].map(len).max()))
    print("--\n")

    races = list(pd.unique(df["race"]))
    data_dict = {}
    for r in races:
        data_dict[r] = {}
        data_dict[r]["race"] = r
        data_dict[r]["name_list"] = df[df["race"] == r]["name"]
        data_dict[r]["char_list"] = sorted(list(set(data_dict[r]["name_list"].str.cat() + "*")))
        data_dict[r]["char_to_num"] = { ch: i for i, ch in enumerate(data_dict[r]["char_list"])}
        data_dict[r]["ix_to_char"] = { i:ch for i, ch in enumerate(data_dict[r]["char_list"])}

        for k, v in data_dict.items():
            print('group: {}'.format(k))
            print('  - number of names: {} ({}, ...)'.format(len(v['name_list']), v['name_list'][:5].tolist()))
            print('  - number of chars: {}'.format(len(v['char_list'])))
            print('  - chars: {}'.format(v['char_list']))
            print('  - char_to_num: {}'.format(v['char_to_num']))
            print('  - ix_to_char: {}'.format(v['ix_to_char']))
            print('######################')

create_names()
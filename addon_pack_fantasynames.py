import random



import pandas as pd; import numpy as np; from bs4 import BeautifulSoup
import requests; import os; import re; import addon_pack_namegen
from pandas import json_normalize; import json
from unidecode import unidecode

def find_names():


    with open('xgtenames.json') as f:
        data = json.load(f)
    print(data)
    titles = json_normalize(data, ["name"])
    print(titles)
    catagories = json_normalize(data, ["name", "tables"])
    print(catagories)
    un_nested = json_normalize(data, ["name", "tables", "table"],errors="ignore", meta_prefix="name_")
    
    print(un_nested)
    print(pd.unique(un_nested.columns))

    #Json data instead; https://github.com/TheGiddyLimit/TheGiddyLimit.github.io/blob/master/data/names.json - https://datatofish.com/load-json-pandas-dataframe/
    #Because of how the PDF is set out, the names need to be split - No longer using the PDF time for more webscraping !


find_names()
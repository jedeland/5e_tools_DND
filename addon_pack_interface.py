import pandas as pd; import numpy as np
import requests; import os; import re; import addon_pack_namegen

from unidecode import unidecode
def npc_options():
    if os.path.exists("names_merged.xlsx"):
        df_arg = pd.read_excel("names_merged.xlsx")
        print("Loading NPC options....")
        print("Type the number of NPC's you wish to create: ")
        npc_num = input(": ")

    else:

        create_npc(False)


def create_npc(exists):
    if exists:
        print("Retrieving NPC's ...")
    elif exists is not True:
        print("The file does not currently exist\n"
              "Creating new file, this may take a while....")
        df = addon_pack_namegen.splice_names()
        npc_options()
npc_options()
import pandas as pd; import numpy as np
import requests; import os; import re; import addon_pack_namegen

from unidecode import unidecode
def npc_options():
    if os.path.exists("names_merged.xlsx"):
        npc_data_exists(True)
        df_arg = pd.read_excel("names_merged.xlsx")
        print("Loading NPC options....")
        culture_list = pd.unique(df_arg["origin"])

        print(culture_list, len(culture_list))
        africa = culture_list.choose(0, 2, 8, 69)
        arabia =  culture_list[3, 4, 6, 27, 31, 35, 38, 63, 64]
        asia = culture_list[14, 16, 25, 34, 30, 35, 37:39, 47, 48, 51, 56, 67, 68]
        europe = culture_list.pop(0, 2, 3, 8, 69 ,14, 16, 25, 34, 30, 35, 37, 38, 39, 47, 48, 51, 56, 67, 68)
        print(europe)



        #Assigns cultural lists to regions
        regions = {"Africa": africa, "Europe": europe,"Near East": arabia, "Asia": asia}
        print("Type the number of NPC's you wish to create: ")
        npc_num = None
        while npc_num is None:
            try:
                num_arg = int(input(""))
                if num_arg >= 101 or num_arg <= 0:
                    print("The program can only create less than 100 NPC's, try again")
                else:
                    npc_num = num_arg
            except:
                print("There was an error, please ensure the input is a valid number")
        print("Are the NPC's the same culture as each other? [y/n]")
        group_culture = None
        yes_list, no_list = ["y", "yeh", "yes", "yep"], ["n", "no", "nah", "nope"]
        while group_culture is None:
            try:
                group_culture = input("")
                if group_culture.lower() in yes_list:
                    print("Creating NPC's with the same culture")
                    group_culture = True
                elif group_culture.lower() in no_list:
                    print("Creating NPC's with different cultures")
                    group_culture = False
            except:
                print("There was an error, please ensure the input corresponds to yes or no")
        culture_list = pd.unique(df_arg["origin"])
        if group_culture is True or npc_num == 1:
            print("Please select the NPC('s) culture region")
            for number, origin in enumerate(culture_list, start=1):
                print(number," ", origin)




    else:

        npc_data_exists(False)


def npc_data_exists(exists):
    if exists:
        print("Retrieving NPC's ...")
    elif exists is not True:
        print("The file does not currently exist\n"
              "Creating new file, this may take a while....")
        df = addon_pack_namegen.splice_names()
        npc_options()
npc_options()
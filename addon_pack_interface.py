import pandas as pd; import numpy as np
import requests; import os; import re; import addon_pack_namegen

from unidecode import unidecode
def npc_options():
    if os.path.exists("names_merged.xlsx"):
        npc_data_exists(True)
        df_arg = pd.read_excel("names_merged.xlsx")
        print("Loading NPC options....")
        culture_list = pd.unique(df_arg["origin"])
        culture_list = culture_list.tolist()
        print(culture_list, len(culture_list), type(culture_list))

        af_num = [0, 2, 8, 69]
        africa = [culture_list[g] for g in af_num]

        arb_num = [3, 4, 6, 27, 31, 35, 38, 63, 64]
        arabia = [culture_list[v] for v in arb_num]
        as_num = [14, 16, 25, 34, 30, 35, 37, 38, 39, 47, 48, 51, 56, 67, 68]
        asia = [culture_list[p] for p in as_num]
        for number, origin in enumerate(culture_list, start=0):
            print(number, " ", origin)
        euro_num = [1, 4, 5, 6, 7, 9, 10, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29,
                    31, 32, 33, 36, 38, 40, 41, 42, 43, 44, 45, 46, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59,
                    60, 61, 62, 63, 64, 65]
        europe = [culture_list[n] for n in euro_num]
        print(europe)



        #Assigns cultural lists to regions
        regions = {"Africa": africa, "Europe": europe,"Near East": arabia, "Asia": asia}
        print(regions)
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
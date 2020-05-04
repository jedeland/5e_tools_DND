import pandas as pd; import numpy as np
import requests; import os; import re; import addon_pack_namegen

from unidecode import unidecode
def npc_options():
    if os.path.exists("names_merged.xlsx"):
        df_arg = pd.read_excel("names_merged.xlsx")
        print("Loading NPC options....")

        print("Type the number of NPC's you wish to create: ")
        npc_num = None
        while npc_num is None:
            try:
                num_arg = int(input(""))
                if num_arg > 101 or num_arg < 0:
                    print("The program can only create less than 100 NPC's, try again")
                else:
                    npc_num = num_arg
            except:
                print("There was an error, please ensure the input is a valid number")
        print("Are the NPC's the same culture as each other? [y/n]")
        culture_arg = None
        yes_list, no_list = ["y", "yeh", "yes", "yep"], ["n", "no", "nah", "nope"]
        while culture_arg is None:
            try:
                culture_arg = input("")
                if culture_arg.lower() in yes_list:
                    print("Creating NPC's with the same culture")
                    culture_arg = "yes"
                elif culture_arg.lower() in no_list:
                    print("Creating NPC's with different cultures")
            except:
                print("There was an error, please ensure the input corresponds to yes or no")

        for i in range(npc_num):
            break



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
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
        do_enum(culture_list)
        non_relevant = []

        bad_boy_list = []
        for i in culture_list:
            df_temp = df_arg.loc[df_arg["origin"] == i]
            print(df_temp)
            if any(df_temp["tag"] != "N"):
                print("This dataframe has regular names")
            else:
                non_relevant.append(i)
                bad_boy_list.append(i)
                print("This dataframe has no regular names")
                print(pd.unique(df_temp["tag"]))

        for g in culture_list:
            df_temp_g = df_arg.loc[df_arg["origin"] == g]
            print(df_temp_g)
            if any(df_temp["tag"] == "N"):
                print("This DF contains last names")
            else:
                print("This DF contains no last names")


        af_num = [0, 8]
        africa = [culture_list[g] for g in af_num]
        arb_num = [3, 4, 6, 29, 33, 36, 57]
        arb_tag = ['Arabia', 'Armenia', 'Azerbaijan', 'Israel', 'Persian', 'Kazakhstan', 'Turkey']
        arabia = [culture_list[v] for v in arb_num]
        as_num = [14, 16, 32, 28, 33, 35, 36, 37, 45, 46, 50, 60]
        as_tag = ['Philippines', 'China', 'India', 'Persian', 'Japan', 'Kazakhstan', 'Korea', 'Pakistani', 'Srilanka', 'Vietnam']
        asia = [culture_list[p] for p in as_num]
        euro_num = ['Albania', 'Armenia', 'Austria', 'Azerbaijan', 'Balkan', 'Basque', 'Russia', 'Belgium', 'France', 'Bulgaria', 'Celtic', 'Czech', 'Denmark', 'Dutch', 'East Frisia', 'England',
                    'Estonia', 'Norway', 'Finland', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latin', 'Latvia', 'Lithuania',
                    'Luxembourg', 'Macedonia', 'Malta', 'Romania', 'Poland', 'Portugal', 'Scandinavian', 'Slavic', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Swiss', 'Turkey', 'Ukraine']
        europe = [culture_list[n] for n in euro_num]
        union_list = [arabia, asia, europe]
        drop_list = []
        for i in union_list:

            for item in i:
                df_temp = df_arg.loc[df_arg["origin"] == item]
                print(df_temp)
                if len(pd.unique(df_temp["tag"])) == 1:
                    drop_list.append(item)
                    i.remove(item)
                else:
                    pass

        print(drop_list, non_relevant)
        #print(arabia, asia, europe)
        print(bad_boy_list)


        #Assigns cultural lists to regions
        regions = {"Europe": europe,"Near East": arabia, "Asia": asia}

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
        origin_list = list(regions.keys())
        if group_culture is True or npc_num == 1:
            print("Please select the NPC('s) culture region")
            do_enum(regions)
            choice = int(input("Number: ")) #Ensures input is int
            dict_arg = origin_list[choice-1] #Lists start at 0
            regions_refined = regions.get(dict_arg)
            do_enum(regions_refined)
            choice = int(input("Number: "))
            selected_nation = regions_refined[choice-1]
            show_npc(df_arg, selected_nation, npc_num)
    else:
        npc_data_exists(False)

def show_npc(df, nations, num_npcs):
    print("Taking random value from data, returning {0} NPC names from {1}".format(num_npcs, nations))

    df = df.loc[df["origin"] == nations]
    rand_name, rand_surname = df.loc[df["tag"] != "N"], df.loc[df["tag"] == "N"]
    for i in range(num_npcs):
        f_name, l_name = np.random.choice(rand_name["name"], 1), np.random.choice(rand_surname["name"],1)
        print(f_name)

        name = str(f_name + " " + l_name)
        name = str(name.title())
        name = re.sub(r'[^\w\s]', '', name)
        print("NPC: {0}".format(name))
    #print(df)

def do_enum(args):
    for number, origin in enumerate(args, start=1):
        print(number, " ", origin)


def npc_data_exists(exists):
    if exists:
        print("Retrieving NPC's ...")
        #Passes through to main function
    elif exists is not True:
        print("The file does not currently exist\n"
              "Creating new file, this may take a while....")
        df = addon_pack_namegen.splice_names()
        npc_options()
npc_options()
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
        for i in culture_list:
            df_temp = df_arg.loc[df_arg["origin"] == i]
            print(df_temp)
            if any(df_temp["tag"] != "N"):
                print("This dataframe has regular names")
            else:
                non_relevant.append(i)

                print("This dataframe has no regular names")
                print(pd.unique(df_temp["tag"]))
        non_relevant_last = []
        for g in culture_list:
            df_temp_g = df_arg.loc[df_arg["origin"] == g]
            print(df_temp_g)
            if any(df_temp_g["tag"] == "N"):
                print("This DF contains last names")
            else:
                non_relevant_last.append(g)

                print("This DF contains no last names")


        af_num = [0, 8]
        af_tag = ["African"]
        africa = [culture_list[g] for g in af_num]
        arb_num = [3, 4, 6, 29, 33, 36, 57]
        arb_tag = ['Arabia', 'Armenia', 'Azerbaijan', 'Israel', 'Persian', 'Kazakhstan', 'Turkey']
        arabia = [culture_list[v] for v in arb_num]
        as_num = [14, 16, 32, 28, 33, 35, 36, 37, 45, 46, 50, 60]
        as_tag = ['Philippines', 'China', 'India', 'Persian', 'Japan', 'Kazakhstan', 'Korea', 'Pakistani', 'Srilanka', 'Vietnam']
        asia = [culture_list[p] for p in as_num]
        euro_tag = ['Albania', 'Armenia', 'Austria', 'Azerbaijan', 'Balkan', 'Basque', 'Russia', 'Belgium', 'France', 'Bulgaria', 'Celtic', 'Czech', 'Denmark', 'Dutch', 'East Frisia', 'England',
                    'Estonia', 'Norway', 'Finland', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latin', 'Latvia', 'Lithuania',
                    'Luxembourg', 'Macedonia', 'Malta', 'Romania', 'Poland', 'Portugal', 'Scandinavian', 'Slavic', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Swiss', 'Turkey', 'Ukraine']
        europe = euro_tag
        union_list = [arabia, asia, europe]
        union_text_list = [arb_tag, as_tag, euro_tag]
        drop_list = []
        for i in union_list:

            for item in i:
                df_temp = df_arg.loc[df_arg["origin"] == item]
                #print(df_temp)
                if len(pd.unique(df_temp["tag"])) == 1:
                    drop_list.append(item)
                    i.remove(item)
                else:
                    pass

        #print(drop_list, non_relevant)
        #print(arabia, asia, europe)
        #print(non_relevant_last, bad_boy_list)
        #Clean dataframe to remove "does not exist" issues
        df_arg = create_duplicate_names(df_arg, non_relevant_last, non_relevant)
        temp = df_arg[(df_arg["origin"] == "East Frisia")]
        print(pd.unique(temp["tag"]))
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

        name = str(f_name + " " + l_name)
        name = str(name.title())
        name = re.sub(r'[^\w\s]', '', name)
        print("NPC: {0}".format(name))
    #print(df)

def do_enum(args):
    for number, origin in enumerate(args, start=1):
        print(number, " ", origin)

def create_duplicate_names(df, add_last_names, remove_or_add):
    print("Dataframe argument: ", df)

    print("Names to add last names to, please implement these names in the addon_pack_namegen.py file if any adequate data sources are found: ", add_last_names)
    #https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Pr%C3%A9noms_masculins_en_pirah%C3%A3 - Native american
    #https://fr.wiktionary.org/wiki/Annexe:Liste_de_pr%C3%A9noms_b%C3%A9t%C3%A9 - African
    #https://en.wikipedia.org/wiki/Category:Yoruba_given_names - African
    url_dict = {"African": "https://fr.wiktionary.org/wiki/Annexe:Liste_de_pr%C3%A9noms_b%C3%A9t%C3%A9", "Yoruba": "https://en.wikipedia.org/wiki/Category:Yoruba_given_names",
                "Ethiopia": "https://en.wikipedia.org/wiki/Category:Ethiopian_given_names"}
    name_fin = ["Zobe", "Yinka", "Zewde"]
    df = addon_pack_namegen.add_stragglers(df, url_dict, name_fin)
    if "Unisex" in add_last_names:
        add_last_names.remove("Unisex")
    print("Names to remove or add first names to: ", remove_or_add)
    last_name_donor = ["Germany", "Dutch", "Norway", "Balkan"]
    for i in range(len(add_last_names)):
        #print(i)
        df_temp = df[(df["origin"] == last_name_donor[i]) & (df["tag"] == "N")]
        print(df_temp)
        df_x = df_temp.copy() #Supresses copy warning, otherwise useless
        df_x["origin"] = df_x["origin"].replace(str(last_name_donor[i]), str(add_last_names[i]))
        print(df_x.tail(10))
        frames = [df, df_x]
        df = pd.concat(frames, ignore_index=True)
        print(df)
    return df


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
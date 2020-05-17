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
        #do_enum(culture_list)
        non_relevant = []
        for i in culture_list:
            df_temp = df_arg.loc[df_arg["origin"] == i]
            #print(df_temp)
            if any(df_temp["tag"] != "N"):
                pass
                #print("This dataframe has regular names")
            else:
                non_relevant.append(i)

                #print("This dataframe has no regular names")
                #print(pd.unique(df_temp["tag"]))
        non_relevant_last = []
        for g in culture_list:
            df_temp_g = df_arg.loc[df_arg["origin"] == g]
            #print(df_temp_g)
            if any(df_temp_g["tag"] == "N"):
                pass
                #print("This DF contains last names")
            else:
                non_relevant_last.append(g)

                #print("This DF contains no last names")


        af_tag = ["African", "Ethiopia"]
        arb_tag = ['Arabia', 'Armenia', 'Azerbaijan', 'Israel', 'Persian', 'Kazakhstan', 'Turkey']
        arabia = arb_tag
        as_tag = sorted(['Philippines', 'China', 'India', 'Persian', 'Japan', 'Kazakhstan', 'Korea', 'Pakistani', 'Srilanka', 'Vietnam', "Hawaiian"])
        asia = as_tag
        euro_tag = sorted(['Albania', 'Armenia', 'Austria', 'Azerbaijan', 'Balkan', 'Basque', 'Russia', 'Belgium', 'France', 'Bulgaria', 'Celtic', 'Czech', 'Denmark', 'Dutch', 'East Frisia', 'England',
                    'Estonia', 'Norway', 'Finland', 'Georgia', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Italy', 'Latin', 'Latvia', 'Lithuania',
                    'Luxembourg', 'Macedonia', 'Malta', 'Romania', 'Poland', 'Portugal', 'Scandinavian', 'Slavic', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Swiss', 'Turkey', 'Ukraine'])
        europe = euro_tag
        union_list = [arabia, asia, europe]
        union_text_list = [af_tag, arb_tag, as_tag, euro_tag]
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
        temp = df_arg[(df_arg["origin"] == "Ethiopia")]
        print(pd.unique(temp["tag"]))
        #Assigns cultural lists to regions
        regions = {"African": af_tag, "Europe": europe,"Near East": arabia, "Asia": as_tag}

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

        origin_list = list(regions.keys())
        if group_culture is True or int(npc_num) == 1:
            selected_nation = select_group(origin_list, regions)
            show_npc(df_arg, selected_nation, npc_num)
        elif group_culture is False:
            print("Please type the number of different NPC groups you wish to create, each with their own culture")
            group_iter = int(input("Groups: "))
            npc_out = divide_npc_multiculture(npc_num, group_iter)
            print("Group sizes are", npc_out)
            for i in npc_out:
                print("Selecting NPC's for the Group with size {}".format(npc_out))
                selected_nation = select_group(origin_list, regions)
                show_npc(df_arg, selected_nation, npc_num)
            #print(groupings)





    else:
        npc_data_exists(False)


def select_group(origin_list, regions):
    print("Please select the NPC('s) culture region")
    do_enum(regions)
    choice = int(input("Number: "))  # Ensures input is int
    dict_arg = origin_list[choice - 1]  # Lists start at 0
    regions_refined = regions.get(dict_arg)
    do_enum(regions_refined)
    choice = int(input("Number: "))
    selected_nation = regions_refined[choice - 1]
    return selected_nation


def divide_npc_multiculture(npc_num, group_iter):
    print("NPC Total: {}".format(npc_num))
    groupings = []
    npc_calc = npc_num
    for i in range(group_iter):
        try:

            print("Please type the size of Group {}".format(i + 1))
            size_arg = input("Size: ")
            npc_calc = npc_calc - int(size_arg)
            if npc_calc >= 0:

                groupings.append(int(size_arg))
                print("{} NPC's remaining".format(npc_calc))
            elif npc_calc < 0:
                print("\n\n\nOne of your groups is invalid, restarting selection"
                      "\nPlease ensure that your groups do not exceed the NPC total of {0}".format(npc_num))
                divide_npc_multiculture(npc_num, group_iter)

        except:
            print("There are still NPC's remaining, please ensure your groups fill the NPC requirements")
    return groupings


def show_npc(df, nations, num_npcs):
    #Add information about gender of NPC, as some languages are hard to see the difference between
    print("Taking random value from data, returning {0} NPC names from {1}".format(num_npcs, nations))
    df = df.loc[df["origin"] == nations]
    df_num = df["name"].str.contains("[0-9]+", regex=True) #Simple way to filter out any results with numbers in
    df = df[~df_num] #Returns all non-valid results, aka ones that dont fit the regex pattern
    rand_name, rand_surname = df.loc[df["tag"] != "N"], df.loc[df["tag"] == "N"]
    for i in range(num_npcs):
        f_name, l_name = np.random.choice(rand_name["name"], 1), np.random.choice(rand_surname["name"],1)
        #Verifies if names are made up of char's
        name = str(f_name + " " + l_name)
        name = str(name.title())
        #Investigate numeric names in arabic name list, should of been fixed using the str.contains line above
        #print(name)
        name = re.sub(r'[^\w\s]', '', name)
        print("NPC: {0}".format(name))
    #print(df)







def do_enum(args):
    for number, origin in enumerate(args, start=1): #cleaner that using enumerate constantly
        print(number, " ", origin)

def create_duplicate_names(df, add_last_names, remove_or_add):
    print("Dataframe argument: ", df)

    print("Names to add last names to, please implement these names in the addon_pack_namegen.py file if any adequate data sources are found: ", add_last_names)
    #https://fr.wiktionary.org/wiki/Cat%C3%A9gorie:Pr%C3%A9noms_masculins_en_pirah%C3%A3 - Native american
    #https://fr.wiktionary.org/wiki/Annexe:Liste_de_pr%C3%A9noms_b%C3%A9t%C3%A9 - African
    #https://en.wikipedia.org/wiki/Category:Yoruba_given_names - African
    #The URL's below are ones that where non valid, but i found over time new information to make them usable, add any other non valid files here, this could be done in the namegen file
    #But since it is so few results currently it seems like a waste to restart the entire creation process
    url_dict = {"African": "https://fr.wiktionary.org/wiki/Annexe:Liste_de_pr%C3%A9noms_b%C3%A9t%C3%A9", "Yoruba": "https://en.wikipedia.org/wiki/Category:Yoruba_given_names",
                "Ethiopia": "https://en.wikipedia.org/wiki/Category:Ethiopian_given_names", "Hawaiian": "https://en.wiktionary.org/wiki/Category:Hawaiian_male_given_names",
                "Hawf": "https://en.wiktionary.org/w/index.php?title=Category:Hawaiian_female_given_names&pageuntil=POLI%CA%BBAHU%0APoli%CA%BBahu#mw-pages"}
    name_fin = ["Zobe", "Yinka", "Zewde", "ʻŌpūnui", "Piʻilani"]
    df = addon_pack_namegen.add_stragglers(df, url_dict, name_fin)
    if "Unisex" in add_last_names:
        add_last_names.remove("Unisex")
    print("Lists to remove or add first names to, if has not already been done via\nadd_stragglers(): ", remove_or_add)
    #Add new elemnt to last_name_donor if the add_last_names list expands, uses and copies pre existing last names for values without last names
    last_name_donor = ["Germany", "Dutch", "Norway", "Balkan"]
    for i in range(len(add_last_names)):

        df_temp = df[(df["origin"] == last_name_donor[i]) & (df["tag"] == "N")]
        df_x = df_temp.copy() #Supresses copy warning, otherwise useless
        #Replaces value I with value I from both lists, for instance if I = 0 then the copied Germany values will be replaced with Austria
        df_x["origin"] = df_x["origin"].replace(str(last_name_donor[i]), str(add_last_names[i]))
        #print(df_x.tail(10))
        frames = [df, df_x]
        #Merges copied values into existing dataframes
        df = pd.concat(frames, ignore_index=True)
        #print(df)
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
import random



import pandas as pd; import numpy as np; from bs4 import BeautifulSoup
import requests; import os; import re; import addon_pack_namegen
from pandas import json_normalize; import json
from unidecode import unidecode

import tensorflow.python.compat as tf
from tensorflow.python.keras.layers import Activation, Input, SimpleRNN, Dense, LSTM
from tensorflow.python.keras.models import Model, Sequential, model_from_json
from tensorflow.python.keras.optimizers import Adam
from tensorflow.keras import utils
from tensorflow.python.framework.ops import disable_eager_execution

disable_eager_execution()

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

    for g in races:
        x, y, train_util, train_info = training_data(g, data_dict, 3)
        print(train_util)
        current_model, training_infos, history =model_start(train_info, 128)
        compile_model(model=current_model,
                      hyperparams={"lr":0.003, "loss": "categorical_crossentropy", "batch_size":32},
                      history=history, training_infos=training_infos)
        train_model(current_model, x, y, training_infos, history, 5)
    print("Did that work?")

def training_data(target_group, data_dict, len_sequence):
    print(target_group)
    train_names = data_dict[target_group]["name_list"].tolist()
    padd_start, padd_end = train_names[0][0], train_names[0][-1] #First element of list, with first and last character id'd
    char_to_index = data_dict[target_group]["char_to_num"]
    index_to_char = data_dict[target_group]["ix_to_char"]

    num_chars = len(data_dict[target_group]["char_list"])
    trainable_names = [padd_start * (len_sequence - 1) + n + padd_end * (len_sequence - 1) for n in train_names]
    x_list, y_list = [], []
    for name in train_names:
        for i in range(max(1, len(name) - len_sequence)):
            new_seq = name[i:i+len_sequence]
            target_char = name[i + len_sequence]

            x_list.append([utils.to_categorical(char_to_index[c], num_chars) for c in new_seq])
            y_list.append(utils.to_categorical(char_to_index[target_char], num_chars))
    x = np.array(x_list)
    y = np.array(y_list)

    m = len(x)
    trainset_infos = {
        'target_group': target_group,
        'length_of_sequence': len_sequence,
        'number_of_chars': num_chars,
        'm': m,
        'padding_start': padd_start,
        'padding_end': padd_end,
    }

    out_dict = {"c2i": char_to_index, "i2c": index_to_char}
    return x, y, out_dict, trainset_infos

def model_start(trainset_infos, lstm_units):
    len_seq = trainset_infos["length_of_sequence"]
    num_char = trainset_infos["number_of_chars"]

    x_in = Input(shape=(len_seq, num_char))

    x = LSTM(units=lstm_units)(x_in) #Default 256
    x = Dense(units=num_char)(x)

    output = Activation("softmax")(x)

    model = Model(inputs=x_in, outputs= output)
    training_infos = {
        'total_epochs': 0,
        'loss': 0,
        'acc': 0,
        'trainset_infos': trainset_infos,
    }
    history = {
        'loss': np.array([]),
        'acc': np.array([]),
        'hyperparams': []
    }
    model.summary()
    return model, training_infos, history
def compile_model(model, hyperparams, history, training_infos):
    optimizer  = Adam(lr=hyperparams["lr"])
    model.compile(loss=hyperparams["loss"], optimizer = optimizer, metrics = ["accuracy"])
    history["hyperparams"].append((training_infos["total_epochs"], hyperparams))
    print("\n\n\n", "History of params", history["hyperparams"])

    return None

def 

create_names()
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
    #df = df.loc[~(df["option"] == "Clan")]
    df = df.loc[~(df["option"] == "Virtue")]
    df = df.loc[~(df["option"] == "Duergar Clan")]
    #df = df.loc[~(df["option"] == "Family")]
    # option_names = ['Female', 'Male', 'Child', 'Female Adult', 'Male Adult']
    # for i in option_names:
    #     df = df.loc[~(df["option"] == i)]

    #"Virtue", "Duergar Clan", "Family"])]

    print('Max name size: {}'.format(df['name'].map(len).max()))
    print("--\n")

    races = list(pd.unique(df["race"]))
    origins = list(pd.unique(df["option"]))
    print(origins)
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
    names_dict = {}
    for g in races:

        x, y, train_util, train_info = training_data(g, data_dict, 3)
        #print(train_util)
        current_model, training_infos, history =model_start(train_info, 178) #Original used 128, 256 is too slow
        compile_model(model=current_model,
                      hyperparams={"lr":0.003, "loss": "categorical_crossentropy", "batch_size":32},
                      history=history, training_infos=training_infos)
        train_model(current_model, x, y, training_infos, history, 2200) #Epochs after 2000 seem efficient
        print("Printing {} names".format(g))
        name_list = []
        name_list = set(name_list)
        i = 0
        vowels = "aeiou"
        while i < 950:
            name = generate_name(
                model=current_model,
                trainset_infos=train_info,
                #         sequence_length=trainset_infos['length_of_sequence'],
                train_util=train_util,
                #         padding_start=padding_start,
                #         padding_end=padding_end,
                name_max_length=15)
            if len(name) >= 3 and int(name.lower().count("z")) < 4:

                vow_check = [vow for vow in name.lower() if vow in vowels]
                if len(vow_check) >= 1:
                    name_list.add(name.title())
            i += 1
        print(i)
        print(len(name_list))
        name_list = sorted(name_list)
        names_dict.update({g: list(name_list)})
        print(names_dict)

    print("Did that work?")
    return names_dict

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
        'accuracy': np.array([]),
        'hyperparams': []
    }
    model.summary()
    return model, training_infos, history
def compile_model(model, hyperparams, history, training_infos):
    optimizer  = Adam(lr=hyperparams["lr"])
    model.compile(loss=hyperparams["loss"], optimizer = optimizer, metrics = ["accuracy"])
    history["hyperparams"].append((training_infos["total_epochs"], hyperparams))
    #print("\n\n\n", "History of params", history["hyperparams"])

    return None

def train_model(model, x, y, training_infos, history, epochs_to_add = 100):

    #history["acc"] = history.pop("accuracy")
    #history["hyperparams"] = history.pop("hyperparams")
    old_loss = training_infos['loss']
    old_acc = training_infos['acc']
    # Extract hyperparams to fit the model
    hyperparams = history['hyperparams'][-1][1]

    # Train the model
    training_model = model.fit(
        x, y,
        batch_size=hyperparams['batch_size'],
        initial_epoch=training_infos['total_epochs'],
        epochs=training_infos['total_epochs'] + epochs_to_add
    )

    # Update history
    for key, val in training_model.history.items():

        history[key] = np.append(history[key], val)

    # Update the training session info
    training_infos['total_epochs'] += epochs_to_add
    training_infos['loss'] = history['loss'][-1]
    training_infos['acc'] = history['accuracy'][-1]

    return None

def generate_name(
        model, trainset_infos, train_util,
        name_max_length = 25
        ):
    dict_size = trainset_infos["number_of_chars"]
    seq_len = trainset_infos["length_of_sequence"]
    index_to_char = train_util["i2c"]
    char_to_index = train_util["c2i"]
    padd_start = trainset_infos["padding_start"]
    generated_name = padd_start * (seq_len + name_max_length)
    probability = 1
    gap = 0
    for i in range(name_max_length):
        x_char = generated_name[i:i+seq_len]
        x_cat = np.array([[utils.to_categorical(char_to_index[c], dict_size) for c in x_char]])
        p = model.predict(x_cat)
        best_char, best_char_prob = index_to_char[np.argmax(p)], np.max(p)

        new_char_index = np.random.choice(range(dict_size), p = p.ravel())
        new_char_prob = p[0][new_char_index]

        new_char = index_to_char[new_char_index]
        generated_name = generated_name[:seq_len+i] + new_char + generated_name[seq_len+i+1:]
        probability *= new_char_prob
        gap += best_char_prob-new_char_prob
        # print(
        #     'i={} new_char: {} ({:.3f}) [best:  {} ({:.3f}), diff: {:.3f}, prob: {:.3f}, gap: {:.3f}]'.format(
        #         i, new_char,new_char_prob,
        #         best_char,best_char_prob,
        #         best_char_prob - new_char_prob,
        #         probability,gap
        #     ))
        if new_char == trainset_infos['padding_end']:
            break
    generated_name = generated_name.strip("#*")
    print(generated_name.title())
    #print('{} (probs: {:.6f}, gap: {:.6f})'.format(generated_name, probability, gap))
    return generated_name #, {'probability': probability, 'gap': gap}



create_names()
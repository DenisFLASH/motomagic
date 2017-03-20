# -*- coding: utf-8 -*-

import configparser
import os

CFG_FOLDER = 'config'

def read_config(cfg_filename):
    """
    Load properties from configuration file into ConfigParser object.

    :param cfg_filename: path to configuration file
    :return: ConfigParser object after readi
    """
    path = os.path.join(CFG_FOLDER, cfg_filename)
    config = configparser.ConfigParser()
    if (os.path.exists(path)):
        config.read(path)
    else:
        print("path does not exist:", path)
        print(os.getcwd())
    return config

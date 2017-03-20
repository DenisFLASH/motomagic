# -*- coding: utf-8 -*-

import MySQLdb as mdb
from motomagic.tools.read_config import read_config

config = read_config('database.properties')
ENV = 'dev'
DB_HOST       = config.get(ENV+'.mysql','dbHost')
DB_USER      = config.get(ENV+'.mysql','dbUser')
DB_PASSWORD       = config.get(ENV+'.mysql','dbPwd')
DB_NAME      = config.get(ENV+'.mysql','dbName')


def create_block_table():
    """
    Create a table for writers and insert some data into it
    """
    db = mdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with db:
        cursor = db.cursor()
        sql_drop_table = "DROP TABLE IF EXISTS block;"
        sql_create_table = "CREATE TABLE block (" \
                "block_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                "device_id VARCHAR(50) NOT NULL," \
                "block_start_time DATETIME NOT NULL," \
                "block_size FLOAT NOT NULL," \
                "filtered_ratio FLOAT NOT NULL," \
                "PRIMARY KEY (block_id)" \
              ") ENGINE=INNODB;"
        cursor.execute(sql_drop_table)
        print("SQL: table 'block' dropped")
        cursor.execute(sql_create_table)
        print("SQL: table 'block' created")


#def insert_block(device_id, block_start_time, block_length, filtered_ratio):
def insert_block(block):
    """
    Insert a block into the 'block' table of the database.

    Parameters
    ----------
    block : Block
        block of data

    Returns
    -------
    int
        number of inserted blocks
    """
    db = mdb.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    with db:
        cursor = db.cursor()
        sql_insert_block = "INSERT INTO block " \
                           "(device_id, block_start_time, block_size, filtered_ratio) VALUES " \
                           "('{}', '{}', {}, {});".format(block.device_id, block.start_time, block.size, block.filtered_ratio)
        cursor.execute(sql_insert_block)
        print("block inserted into database")


if __name__ == '__main__':
    create_block_table()

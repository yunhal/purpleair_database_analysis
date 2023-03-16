# -*- coding: utf-8 -*-
"""
This code gets real-time PurpleAir data of one site every 
few minutes to build your own database.

Data from the site are in bytes/text and NOT in JSON format.

Created on Fri Dec 02, 11:52:10 2022

This code is heavily modified from the code by Zuber Farooqui, Ph.D. 
: https://github.com/zfarooqui/py_purpleair_aqi

@author: Yunha Lee, Ph.D.

"""
from purpleair import PurpleAir
import requests
import pandas as pd
import os
from datetime import datetime
import time
import json
from io import StringIO
import sqlalchemy as db
import schedule

def flatten_json(data: dict) -> dict:
  
    flat_data = dict()
    for key, value in data.items():
        if not isinstance(value, dict):
            flat_data[key] = value
        else:

            # 1st nested item
            for k, v in value.items():
                if (k == "stats_a"):
                    print("not saving stats_a information ", k)
                else:

                    if not isinstance(v, dict):
                        flat_data[key + "_" + k] = v
                    else:

                        # 2nd nested items
                        for k2, v2 in v.items():
                            if not isinstance(v2, dict):
                                flat_data[key + "_"+ k+ "_"+ k2] = v2
                            else: 

                                # 3rd nested items
                                for k3, v3 in v.items():
                                    if not isinstance(v3, dict):
                                        flat_data[key + "_"+ k+ "_"+ k2+ "_"+ k3] = v3
                                    else:
                                        print("WARNING: this json file has more than 3rd nested layers")
      
    return flat_data

def get_PA_data(key_read, sensor_id):

    """
    Parameters
    ----------
    key_read : your PurpleAir API key 
    sensor_id : ID number of the sensor you want to read
    """

    # get real-time sensor data 
    p = PurpleAir(key_read)
    json_data = p.get_sensor_data(sensor_id)

    # Flatten multi-nested json data to a dictionary
    flat_data = flatten_json(data= json_data)

    # Create a pandas dataframe 
    df = pd.DataFrame(flat_data, index=[0])

    return df

def create_sql_csv (save_as_sql=True, save_as_csv=True):
    """
    Parameters
    ----------
    key_read : your PurpleAir API key 
    sensor_id : ID number of the sensor you want to read
    save_as_sql : Boolean value to save the data as SQLite 
    save_as_csv : Boolean value to save the data as CSV
    """

    df = get_PA_data(key_read, sensor_id)

    # Writing to SQLite Table (Optional)
    sql_tablename = 'purpleair_' + sensor_id
    df.to_sql(sql_tablename, con=engine, index=False)

    # writing to csv file
    csv_filename = db_path + '/sensor_index_' + sensor_id + '.csv'
    df.to_csv(csv_filename, index=False, header=True)

    return

def append_sql_csv (save_as_sql=True, save_as_csv=True):
    """
    Parameters
    ----------
    key_read : your PurpleAir API key 
    sensor_id : ID number of the sensor you want to read
    save_as_sql : Boolean value to save the data as SQLite 
    save_as_csv : Boolean value to save the data as CSV
    """

    df = get_PA_data(key_read, sensor_id)

    # Writing to SQLite Table (Optional)
    sql_tablename = 'purpleair_' + sensor_id
    df.to_sql(sql_tablename, con=engine, if_exists='append', index=False)

    # writing to csv file
    csv_filename = db_path + '/sensor_index_' + sensor_id + '.csv'
    df.to_csv(csv_filename, index=False, header=False, mode='a')

    return

##########################################################################

# set a sensor index 
sensor_id = '143856'

# minutes time frequency of generating PA real-time data
pa_time = 2 # according to PA, every 2 minutes

# API Keys provided by PurpleAir(c)
key_dir = "./purpleair_api_read_key"
with open(key_dir) as f:
    key_read = f.readlines()[0]
    key_read = key_read.strip() # could contain whitespace
    print(key_read, len(key_read))

# create database directory
db_path = "./database_" + datetime.now().strftime("%b-%d-%Y-%H_%M_%S")
print("database dir is created : ", db_path)
if not os.path.exists(db_path):
    os.makedirs(db_path)

# Starting engine for SQLite
sql_path = db_path + "/purpleair_"+ sensor_id +".sqlite"
print(f'os.path.abspath(sql_path): {str(os.path.abspath(sql_path))}')
SQL_URI = "sqlite:///" + os.path.abspath(sql_path) 
engine = db.create_engine(SQL_URI)

# create sql and/or csv files
create_sql_csv(save_as_sql=True, save_as_csv=True)

# calling append_sql_csv every two minutes to create historical database from real-time data
schedule.every(pa_time).minutes.do(append_sql_csv, save_as_sql=True, save_as_csv=True)

while True:
    schedule.run_pending()
    time.sleep(60)
from .get_steamlist import getownedgames
from .csv_to_db import db_connect, dataframe_to_sql
from .get_psnlist import getpsngames

#sqlite database parameters
database='sqlite:///db.sqlite3'
table='steamlist_steam_game'

def get_steam_db(apikey, steamid):
    #api key and steamid for data collection
    apikey = apikey
    steamid = steamid

    test_key = True
    if not apikey or not steamid:
        test_key = False
        return test_key

    #csv creation and storage in dataframe
    data = getownedgames(apikey=apikey, steamid=steamid)
    #establishing connection with sqlalchemy
    db = db_connect(database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, table)

def get_psn_db(token):
    
    #api key and steamid for data collection
    token = token

    test_token = True
    if not token:
        test_token = False
        return test_token

    #csv creation and storage in dataframe
    data = getpsngames(token=token)
    print(len(data))
    #establishing connection with sqlalchemy
    db = db_connect(database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, table)

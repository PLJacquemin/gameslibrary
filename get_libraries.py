from .get_steamlist import getownedgames
from .csv_to_db import db_connect, dataframe_to_sql
from .get_psnlist import getpsngames

def get_steam_db(apikey, steamid):
    #api key and steamid for data collection
    apikey = apikey
    steamid = steamid

    #sqlite database parameters
    database='sqlite:///db.sqlite3'
    table='GamesLibrary_video_game'

    #csv creation and storage in dataframe
    data = getownedgames(apikey=apikey, steamid=steamid)
    #establishing connection with sqlalchemy
    db = db_connect(database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, table)

def get_psn_db(token):
    #api key and steamid for data collection
    token = token

    #sqlite database parameters
    database='sqlite:///db.sqlite3'
    table='GamesLibrary_video_game'

    #csv creation and storage in dataframe
    data = getpsngames(token=token)
    print(len(data))
    #establishing connection with sqlalchemy
    db = db_connect(database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, table)
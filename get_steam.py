from .get_libraries import getownedgames
from .csv_to_db import db_connect, dataframe_to_sql
from .get_psnlist import getpsngames

def get_steam_db(apikey, steamid):
    #api key and steamid for data collection
    apikey = apikey
    steamid = steamid

    test_key = True
    if not apikey or not steamid:
        test_key = False
        return test_key

    #postgresql database parameters
    user='postgres'
    password=''
    host='localhost'
    port='5432'
    database='steamlist'
    schema='public'
    table='GamesLibrary_video_game'

    #csv creation and storage in dataframe
    data = getownedgames(apikey=apikey, steamid=steamid)
    #establishing connection with sqlalchemy
    db = db_connect(user,password,host,port,database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, schema, table)

def get_psn_db(token):
    test_token = True
    #api key and steamid for data collection
    token = token

    if not token:
        test_token = False
        return test_token

    #postgresql database parameters
    user='postgres'
    password=''
    host='localhost'
    port='5432'
    database='steamlist'
    schema='public'
    table='GamesLibrary_video_game'

    #csv creation and storage in dataframe
    data = getpsngames(token=token)
    print(len(data))
    #establishing connection with sqlalchemy
    db = db_connect(user,password,host,port,database)
    #databse filling if a ne entry is spotted
    dataframe_to_sql(data, db, schema, table)

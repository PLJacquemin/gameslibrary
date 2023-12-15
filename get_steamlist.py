import json
import pandas as pd
import os.path
import sys
from urllib.request import urlopen
from datetime import date
import sqlite3

data_columns = ['id','name','playtime_forever','img_icon_url','completed','played','date','genre','platform','appid','last_played','img_url','gaas','unfinishable','critic','num_stars','publisher','release_year','update_date']
conn = sqlite3.connect('db.sqlite3', check_same_thread=False)


#fonction pour aller chercher la liste de jeu sur Steam
def getownedgames(apikey, steamid):
    print("*"*50)
    print(apikey)
    print(steamid)
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={apikey}&steamid={steamid}&include_appinfo=1'
    try:
        games=json.loads(urlopen(url).read().decode())['response']['games']
        print("Steam list succesfully obtained")
    except ValueError:
        print("Data collection failed")
        sys.exit()
    print(" "*50)
    
    df_games = pd.DataFrame(games)
    df_to_csv = pd.DataFrame()

    #si premier fichier, création
    if not os.path.exists('steamlist/csv_db/steam_list.csv'):
        df_to_csv['id']=df_games['appid']
        df_to_csv['name']=df_games['name']
        df_to_csv['playtime_forever']=df_games['playtime_forever']
        df_to_csv['img_icon_url']=df_games['img_icon_url']
        df_to_csv['completed']=False
        df_to_csv['played']=False
        df_to_csv['date']="2020-01-01"
        df_to_csv['genre']=""
        df_to_csv['platform']="Steam"
        df_to_csv['appid']=df_games['appid']
        df_to_csv['last_played']="2020-01-01"
        df_to_csv['img_url']=""
        df_to_csv['gaas']=False
        df_to_csv['unfinishable']=False
        df_to_csv['critic']=''
        df_to_csv['num_stars']=5
        df_to_csv['publisher']=''
        df_to_csv['release_year']=1900
        df_to_csv['update_date']="2020-01-01"
        df_to_csv.loc[df_to_csv['playtime_forever']!=0, 'played'] = True
        for game in df_to_csv['name']:
            df_to_csv.loc[df_to_csv['name']==game, 'img_icon_url']=f"http://media.steampowered.com/steamcommunity/public/images/apps/{df_to_csv.loc[df_to_csv['name']==game]['appid'].values[0]}/{df_to_csv.loc[df_to_csv['name']==game]['img_icon_url'].values[0]}.jpg"
            df_to_csv.loc[df_to_csv['name']==game, 'img_url']=f"https://cdn.akamai.steamstatic.com/steam/apps/{df_to_csv.loc[df_to_csv['name']==game]['appid'].values[0]}/header.jpg"


        df_to_csv.to_csv('steamlist/csv_db/steam_list.csv',sep=";", index=False)
        print(f"New file created with {len(df_to_csv)} entries")
        return df_to_csv


    #sinon on ajoute les lignes manquantes
    elif os.path.exists('steamlist/csv_db/steam_list.csv'):
        df_games_new = pd.read_csv('steamlist/csv_db/steam_list.csv', sep=';')
        count=0
        count=0
        for game in df_games['name']:
            if game not in list(df_games_new['name']) :
                df_game = pd.DataFrame([
                    [df_games.loc[df_games['name']==game]['appid'].values[0],
                    game,
                    df_games.loc[df_games['name']==game]['playtime_forever'].values[0],
                    f"http://media.steampowered.com/steamcommunity/public/images/apps/{df_games.loc[df_games['name']==game]['appid'].values[0]}/{df_games.loc[df_games['name']==game]['img_icon_url'].values[0]}.jpg",
                    False,
                    False,
                    '2020-01-01',
                    '',
                    'Steam',
                    df_games.loc[df_games['name']==game]['appid'].values[0],
                    '2020-01-01',
                    f"https://cdn.akamai.steamstatic.com/steam/apps/{df_games.loc[df_games['name']==game]['appid'].values[0]}/header.jpg",
                    False,
                    False,
                    '',
                    5,
                    '',
                    1900,
                    date.today().strftime("%Y-%m-%d")
                    ]],columns=data_columns)
                df_game.loc[df_game['playtime_forever']!=0, 'played'] = True
                df_games_new = pd.concat([df_games_new, df_game], ignore_index=True)    
                print(game)                            
                count+=1
            else:
                if df_games.loc[df_games['name']==game]['playtime_forever'].values[0] != df_games_new.loc[df_games_new['name']==game]['playtime_forever'].values[0]:
                    df_games_new.loc[df_games_new['name']==game, 'playtime_forever'] = df_games.loc[df_games['name']==game]['playtime_forever'].values[0]
                    df_games_new.loc[df_games_new['name']==game, 'update_date'] = date.today().strftime("%Y-%m-%d")
                    print(f"Name {game}, Time {df_games_new.loc[df_games_new['name']==game]['playtime_forever'].values[0]}")
        df_games_new.sort_values('name').to_csv('steamlist/csv_db/steam_list.csv',sep=";", index=False)
        print(f"The existing file was updated with {count} new entries")
        print("*"*50)
        return df_games_new
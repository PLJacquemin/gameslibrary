from psnawp_api import PSNAWP
import os
import pandas as pd
from datetime import date

data_columns = ['id','name','playtime_forever','img_icon_url','completed',
                'played','date','genre','platform','appid','last_played',
                'img_url','gaas','unfinishable','critic','num_stars',
                'publisher','release_year','update_date']

#df_to_csv['id']=df_games['appid']
#df_to_csv['name']=df_games['name']
#df_to_csv['playtime_forever']=df_games['playtime_forever']
#df_to_csv['img_icon_url']=df_games['img_icon_url']
#df_to_csv['completed']=False
#df_to_csv['played']=False
#df_to_csv['date']="2020-01-01"
#df_to_csv['genre']=""
#df_to_csv['platform']="Steam"
#df_to_csv['appid']=df_games['appid']
#df_to_csv['last_played']="2020-01-01"
#df_to_csv['img_url']=""
#df_to_csv['gaas']=False
#df_to_csv['unfinishable']=False
#df_to_csv['critic']=''
#df_to_csv['num_stars']=5
#df_to_csv['publisher']=''
#df_to_csv['release_year']=1900
#df_to_csv['update_date']="2020-01-01"


def getpsngames(token):
    psnawp = PSNAWP(token)
    client = psnawp.me()
    psn_list = list(client.title_stats())
    if not os.path.exists('GamesLibrary/csv_db/psn_list.csv'):
        df_games_new = pd.DataFrame()
        game_count=1
        for game in psn_list:
            df_game=pd.DataFrame([[1000000000+game_count,
                                  game.name,
                                  game.play_duration.seconds//60 + game.play_duration.days * 1440,
                                  game.image_url,
                                  False,
                                  False,
                                  "2020-01-01",
                                  "",
                                  "Playstation",
                                  game.title_id,
                                  game.last_played_date_time.strftime('%Y-%m-%d'),
                                  game.image_url,
                                  False,
                                  False,
                                  '',
                                  5,
                                  '',
                                  1900,
                                  "2020-01-01"]],columns=data_columns)
            df_game.loc[df_game['playtime_forever']!=0, 'played'] = True
            df_games_new = pd.concat([df_games_new, df_game], ignore_index=True)
            game_count+=1
        df_games_new.to_csv('GamesLibrary/csv_db/psn_list.csv',sep=";", index=False)
        return df_games_new
#sinon on ajoute les lignes manquantes
    elif os.path.exists('GamesLibrary/csv_db/psn_list.csv'):
        df_games_new = pd.read_csv('GamesLibrary/csv_db/psn_list.csv', sep=';')
        count=0
        for game in psn_list:
            if game.name not in list(df_games_new['name']) :
                df_game=pd.DataFrame([[df_games_new['id'].max()+1,
                                  game.name,
                                  game.play_duration.seconds//60 + game.play_duration.days * 1440,
                                  game.image_url,
                                  False,
                                  False,
                                  "2020-01-01",
                                  "",
                                  "Playstation",
                                  game.title_id,
                                  game.last_played_date_time.strftime('%Y-%m-%d'),
                                  game.image_url,
                                  False,
                                  False,
                                  '',
                                  5,
                                  '',
                                  1900,
                                  date.today().strftime("%Y-%m-%d")]],columns=data_columns)
                df_game.loc[df_game['playtime_forever']!=0, 'played'] = True
                df_games_new = pd.concat([df_games_new, df_game], ignore_index=True)
                count+=1
            else:
                df_games_new.loc[df_games_new['name']==game, 'playtime_forever'] = game.play_duration.seconds//60 + game.play_duration.days * 1440
                df_games_new.loc[df_games_new['name']==game, 'update_date'] = date.today().strftime("%Y-%m-%d")
                print(f"Name {game}, Time {df_games_new.loc[df_games_new['name']==game]['playtime_forever'].values[0]}")
        df_games_new.sort_values('name').to_csv('GamesLibrary/csv_db/psn_list.csv',sep=";", index=False)
        print(f"The existing file was updated with {count} new entries")
        print("*"*50)
        return df_games_new
    
if __name__ == "__main__":
    getpsngames()
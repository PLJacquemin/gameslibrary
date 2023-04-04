from psnawp_api import PSNAWP
import os
import pandas as pd

data_columns = ['id','name','playtime_forever','img_icon_url','completed','played','date','genre','platform','appid','last_played','img_url']


def getpsngames(token='NJXEoLmknISX0MCdn44bUyFlgKoXHkWNcckN4T0qRvhcQo34gVXbFL4jw5X1gTIN'):
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
                                  game.image_url]],columns=data_columns)
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
                                  game.image_url]],columns=data_columns)
                df_game.loc[df_game['playtime_forever']!=0, 'played'] = True
                df_games_new = pd.concat([df_games_new, df_game], ignore_index=True)
                count+=1
            else:
                df_games_new.loc[df_games_new['name']==game, 'playtime_forever'] = game.play_duration.seconds//60 + game.play_duration.days * 1440
        df_games_new.sort_values('name').to_csv('GamesLibrary/csv_db/psn_list.csv',sep=";", index=False)
        print(f"The existing file was updated with {count} new entries")
        print("*"*50)
        return df_games_new
    
if __name__ == "__main__":
    getpsngames()
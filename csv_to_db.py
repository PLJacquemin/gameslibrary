from sqlalchemy import create_engine, exc, update, Table, MetaData, and_
import numpy as np
from datetime import datetime

import sys

# establish connections
def db_connect(db_database):
    print("*"*50)
    print("Database connection")
    sqlalch_connexion = db_database
    try:
        db_engine = create_engine(sqlalch_connexion)
        print("Connection succesful")
        return db_engine
    except ValueError:
        print("Connection failed")
        sys.exit()

def dataframe_to_sql(db_dataframe, db_engine, db_table):
    meta = MetaData(bind=db_engine)
    MetaData.reflect(meta)
    stable = Table(db_table, meta, extend_existing=True,autoload_with=db_engine)

    for i in range(len(db_dataframe)):
        try:
            db_dataframe.iloc[i:i+1].to_sql(name=db_table, con=db_engine, index=False, if_exists= 'append')
        except exc.IntegrityError:
            pass
        
        stmt = (
            stable.update().values(playtime_forever = int(db_dataframe.iloc[i:i+1]['playtime_forever'].values[0])).where((stable.c.name == db_dataframe.iloc[i:i+1]['name'].values[0])&(stable.c.platform == db_dataframe.iloc[i:i+1]['platform'].values[0]))
            )
        db_engine.execute(stmt)
        stmt = (
            stable.update().values(update_date = datetime.strptime(db_dataframe.iloc[i:i+1]['update_date'].values[0], '%Y-%m-%d')).where((stable.c.name == db_dataframe.iloc[i:i+1]['name'].values[0])&(stable.c.platform == db_dataframe.iloc[i:i+1]['platform'].values[0]))
            )
        db_engine.execute(stmt)
from sqlalchemy import create_engine, exc, update, Table, MetaData, and_
import numpy as np

import sys

# establish connections
def db_connect(db_user,db_password,db_host,db_port,db_database):
    print("*"*50)
    print("Database connection")
    sqlalch_connexion = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
    try:
        db_engine = create_engine(sqlalch_connexion)
        print("Connection succesful")
        return db_engine
    except ValueError:
        print("Connection failed")
        sys.exit()

def dataframe_to_sql(db_dataframe, db_engine, db_schema, db_table):
    meta = MetaData(bind=db_engine)
    MetaData.reflect(meta)
    stable = Table(db_table, meta, extend_existing=True,autoload_with=db_engine)

    for i in range(len(db_dataframe)):
        try:
            db_dataframe.iloc[i:i+1].to_sql(name=db_table, con=db_engine, schema=db_schema, index=False, if_exists= 'append')
        except exc.IntegrityError:
            pass
        
        #stmt = (
        #    stable.update().values(playtime_forever = int(db_dataframe.iloc[i:i+1]['playtime_forever'].values[0])).where((stable.c.name == db_dataframe.iloc[i:i+1]['name'].values[0])&(stable.c.plateform == db_dataframe.iloc[i:i+1]['plateform'].values[0]))
        #    )
        #db_engine.execute(stmt)
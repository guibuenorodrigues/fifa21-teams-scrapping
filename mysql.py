import pymysql
import pandas as pd
from sqlalchemy import create_engine

class Mysql():

    def __init__(self, host:str, user: str, password: str, db: str):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = self.__connect()

    
    def __connect(self) -> pymysql.Connection:

        try:
            conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
            print("Connected to Mysql. Database: {0}".format(self.db))
            return conn
        except Exception:
            raise Exception

    def save_dataframe(self, df:pd.DataFrame):

        
        try:
            engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                        .format(user=self.user, 
                                pw=self.password,
                                host=self.host,
                                db=self.db))

            print("SQL engine create and connected")

            rows_number = len(df.index)
            print("Saving dataframe to Mysql database: {0}. Total of Rows: {1}".format(self.db, rows_number))

            df.to_sql("teams", con=engine, if_exists="append", chunksize=1000, index=False)
        except Exception:
            raise Exception

        

    def select_simple_query(self, table_name: str) -> pd.DataFrame:
        
        try:
            sql_query = "select * from {0}".format(table_name)
            query = pd.read_sql_query(sql_query, self.connection)
            df = pd.DataFrame(query)
            return df
        except Exception:
            raise Exception

    def delete_records(self, table_name: str, where: str = False) -> bool:
        
        w = "where {0}".format(where) if where else ""

        try:
            sql_query = "delete from {0} {1}".format(table_name, w)
            print(sql_query)
        except Exception:
            raise Exception


    def close_connection(self):
        self.connection.close()

       



    

        
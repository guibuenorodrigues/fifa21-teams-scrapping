import mysql
import pandas as pd
import numpy as np


class Repository():

    def __init__(self, host: str, user: str, password: str, db: str):

        self.mysql = mysql.Mysql(host=host, user=user,
                                 password=password, db=db)
        self.first_execution = True

    def dataframe_to_mysql(self, df: pd.DataFrame):

        # clean table on first execution
        if self.first_execution:
            self.mysql.delete_records("teams")

        
        self.mysql.save_dataframe(df)

        


        # for row in df.iterrows():
        #     print(row['Nome'])



    # select row by row and see if exists
        # if exists then update
        # if not then insert

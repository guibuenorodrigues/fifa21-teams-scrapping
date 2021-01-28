import argparse
from scraper import Scrapper
import mysql
import json


if __name__ == "__main__":

   
    # get settings from json file
    with open("settings.json") as json_data_file:
        data = json.load(json_data_file)
                
    sql_host = data['sql']['host']
    sql_user = data['sql']['user']
    sql_pass = data['sql']['pass']
    sql_db = data['sql']['db']



    # get settings from arguments CLI
    arg_parser = argparse.ArgumentParser(
        description='Program to retrieve data from FIFA 21 teams using scrapping...')

    arg_parser.add_argument('--sql_host', action='store', dest='sql_host', default=sql_host,
                            required=False, help='Provide database hostname or IP.')
    arg_parser.add_argument('--sql_user', action='store', dest='sql_user', default=sql_user,
                            required=False, help='Provide database username.')
    arg_parser.add_argument('--sql_pass', action='store', dest='sql_pass', default=sql_pass,
                            required=False, help='Provide database password')
    arg_parser.add_argument('--sql_db', action='store', dest='sql_db', default=str(sql_db),
                            required=False, help='Provide database name.')

    arguments = arg_parser.parse_args()


    print(arguments.sql_db)

    # scrap = Scrapper()
    # df_teams = scrap.get_teams_info('from', 23)

    # m = mysql.Mysql(host=sql_host, user=sql_user, password=sql_pass, db=sql_db)
    # m.save_dataframe(df_teams)

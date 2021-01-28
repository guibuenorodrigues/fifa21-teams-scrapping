from scraper import Scrapper
import mysql

scrap = Scrapper()
df_teams = scrap.get_teams_info()

m = mysql.Mysql(host="localhost", user="root", password="", db="smart_home")
m.save_dataframe(df_teams)



# m = mysql.Mysql("localhost", "root", "", "smart_home")
# m.delete_records("table", "customer=1")




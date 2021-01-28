from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import repository as repo


class Scrapper():

    def __init__(self) -> None:
        self.base_url = "https://www.fifaindex.com"
        self.endpoint = "/pt-br/teams"

    def get_teams_info(self, how: str = 'all', index: int = 1) -> pd.DataFrame:

        request_code = 200
        page_number = 0
        appended_data = []

        while(request_code == 200):

            page_number += 1
            current_page = "{0}{1}/{2}".format(self.base_url, self.endpoint, page_number)
            print("Executing scrapping on page {0} ({1})".format(page_number, current_page))

            # request content
            r = requests.get(current_page)

            # check if content exists
            if r.status_code != 200:
                print("Leaving scrapping. Reason: status code = {0}".format(r.status_code))
                request_code = r.status_code
                break


            #get dataframe result for the page
            df = self.__get_data_from_table(r.content)
            appended_data.append(df)

        
        appended_data = pd.concat(appended_data)
        return appended_data

    
    def __get_data_from_table(self, content: bytes) -> pd.DataFrame:

        # parse content to html
        soup = BeautifulSoup(content, 'html.parser')

        #found table
        table = soup.find_all("table", attrs={"class": "table table-striped table-teams"})

        # validate table content
        if len(table) <= 0:
            raise ValueError("There are no table in the content")

        # select the table if exists
        table_fut = table[0]

        # find TR element
        body = table_fut.find_all("tr")

        # set up the header
        head = body[0]

        # set up the body
        body_rows = body[1:]

        # set up the headings array
        headings = []

        # find all the headers columns
        for item in head.find_all("th"):
            #remove special characters
            item = (item.text).rstrip("\n")
            
            #add to the array
            headings.append(item)

        # set up the rows array
        all_rows = []

        # looping for all body content
        for row_num in range(len(body_rows)):
            # set up the row array
            row = []

            # find all TD elements
            for row_item in body_rows[row_num].find_all("td"):

                # remove special characters
                aa = re.sub("(\xa0)|(\n)|,", "", row_item.text)

                
                img = row_item.find("img")
                data_src = ""

                if img:
                    img_data = str(img['data-srcset'])
                    data_src = img_data.split(',')[0]
                    data_src = data_src[:-3]
                    data_src = "{0}{1}".format(self.base_url, data_src)

                aa = aa.replace('', data_src)



                # add value to the row
                row.append(aa)

            # add row to the array of rows
            all_rows.append(row)


        # create pandas dataframe
        df = pd.DataFrame(data=all_rows, columns=headings)
        df.head()

        df = self.__sanitize_dataframe(df)

        return df
  

    def __sanitize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        
        # remove null rows
        df = df.mask(df.eq('None')).dropna()

        # remove Classificação do time columns
        df = df.drop(labels='Classificação do time', axis=1)

        # rename column names

        columns = {
            '': 'logo',
            'Nome': 'name',
            'Liga': 'league',
            'ATA': 'attack_rating',
            'MEI': 'midfield_rating',
            'DEF': 'defense_rating',
            'GER': 'overall_rating'
        }
        df = df.rename(columns=columns)
        
        # df = df.astype({'attack_rating': 'int32'}).dtypes
        # df = df.astype({'midfield_rating': 'int32'}).dtypes
        # df = df.astype({'defense_rating': 'int32'}).dtypes
        # df = df.astype({'overal_rating': 'int32'}).dtypes



        return df

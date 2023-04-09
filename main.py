from bs4 import BeautifulSoup as bs
from tkinter import Tk
import requests,os
import pandas as pd
import eel

eel.init(os.path.join(os.path.dirname(__file__),'assets'))

class Scraper():
    def __init__(self) -> None:
        self.scrape_standings()
        self.add_header()
        self.add_rows()
        
    def scrape_standings(self):
        target = requests.get('https://www.euroleaguebasketball.net/euroleague/standings/')
        doc = bs(target.text,'html.parser')

        self.main_header = doc.find("div", {"class": "complex-stat-table_row__1P6us"})
        self.table = doc.find_all('div',{"class":'complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez'})

    def add_header(self):
        categories = []
        for category in self.main_header:
            categories.append(category.text)
        return categories

    def add_rows(self):
        row = []    # each row
        rows = []   ## a list of tuples
        for team in self.table:      # take a list of all the elements of table
            for stat in team.contents:     # take all elements of team.contents list, which are the stats     
                row.append(stat.text)
            rows.append(tuple(row)) # turn the list to a tuple and append it to rows
            row.clear() # empty row list, do it all over again
        return rows

    def make_dataset(self):
        dataset = pd.DataFrame(self.add_rows(),columns=self.add_header())
        return dataset

    def clear_dataset(self,df):
        df = df.rename(columns={"PosPositionClub":"Club", "GPGP": "GP", "WWon": "Won", "LLost": "Lost"})
        clubs = []
        for club in df['Club']:
            club = club[1:-4]
            for i in club:
                if i.isdigit():
                    club = club.replace(i,'')
            clubs.append(club)
        df['Club'] = clubs
        return df
    

def scrape():
    scraper = Scraper()
    df = scraper.make_dataset()
    df = scraper.clear_dataset(df)
    return df

def current_standings():
    df = scrape()
    return df.to_dict('records')

@eel.expose 
def get_data():
    return current_standings()


if __name__=='__main__':    
    
    screen_width = Tk().winfo_screenwidth()
    screen_height = Tk().winfo_screenheight()
    width = 1400
    height = 700

    x = (screen_width - width)//2
    y = (screen_height - height)//2

    eel.start('index.html', size=(width, height), position = (x,y))



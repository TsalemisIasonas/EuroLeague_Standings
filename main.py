from bs4 import BeautifulSoup as bs
import requests,os
import pandas as pd
import eel

eel.init(os.path.join(os.path.dirname(__file__),'assets'))

# Function to scrape the standings data from the Euroleague website
def scrape_standings():
    target = requests.get('https://www.euroleaguebasketball.net/euroleague/standings/')
    doc = bs(target.text,'html.parser')

    main_header = doc.find("div", {"class": "complex-stat-table_row__1P6us"})
    table = doc.find_all('div',{"class":'complex-stat-table_row__1P6us complex-stat-table__standingRow__1cfez'})

    def add_header():
        categories = []
        for category in main_header:
            categories.append(category.text)
        return categories

    def add_rows():
        row = []    # each row
        rows = []   ## a list of tuples
        for team in table:      # take a list of all the elements of table
            for stat in team.contents:     # take all elements of team.contents list, which are the stats     
                row.append(stat.text)
            rows.append(tuple(row)) # turn the list to a tuple and append it to rows
            row.clear() # empty row list, do it all over again
        return rows

    def make_dataset():
        dataset = pd.DataFrame(add_rows(),columns=add_header())
        return dataset

    def clear_dataset(df):
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
    
    df = make_dataset()
    df = clear_dataset(df)
    
    return df.to_dict('records')

# Define a function to handle the "get_data" request from the front-end
@eel.expose
def get_data():
    return scrape_standings()

# Start the Eel application
eel.start('index.html', size=(900, 600))



#importing packages
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
#getting per game data
html = urlopen('https://www.basketball-reference.com/leagues/NBA_2018_per_game.html')
soup = BeautifulSoup(html, 'html.parser')
events = soup.find_all("table")[0]
header = events.find_all("thead")[0]
labels = header.find_all("th")
#getting column names
cols = []
for label in labels:
    cols.append(label.string)
#removing rank column and changing name of points per game column
cols.remove('Rk')
cols.remove('PS/G')
cols.append('PPG')
# creating dataframe of every players per game averages
stats = []
temp = []
i=0
contracts = events.find_all('tbody')
players = events.find_all('tr')
for player in players:
    numbers = player.find_all('td')
    for number in numbers:
        temp.append(number.string)
        i = i+1
        if(i%29 == 0):
            stats.append(temp)
            temp = []       
playerstats = pd.DataFrame(stats, columns=cols)
#retreiving advanced statistics data
htmladv = urlopen('https://www.basketball-reference.com/leagues/NBA_2018_advanced.html')
soupadv = BeautifulSoup(htmladv, 'html.parser')
eventsadv = soupadv.find_all("table")[0]
#getting column names
headeradv = eventsadv.find_all("thead")[0]
labelsadv = headeradv.find_all("th")
colsadv = []
for labeladv in labelsadv:
    colsadv.append(labeladv.string)
colsadv.remove('Rk')
#removing the two empty columns from the table
colsadv = [col if col!='\xa0' else 'Temp' for col in colsadv]
#creating the dataframe having each players advanced stats totals
statsadv = []
tempadv = []
i=0
contractsadv = eventsadv.find_all('tbody')
playersadv = eventsadv.find_all('tr')
for playeradv in playersadv:
    numbersadv = playeradv.find_all('td')
    for numberadv in numbersadv:
        tempadv.append(numberadv.string)
        i = i+1
        if(i%28 == 0):
            statsadv.append(tempadv)
            tempadv = []      
playerstatsadv = pd.DataFrame(statsadv, columns=colsadv)
playerstatsadv = playerstatsadv.drop(['Pos','Age','G','MP','Temp'], axis=1)
#joining the tables together to make one large dataset
playerdb = pd.concat([playerstats, playerstatsadv], axis=1)
playerdb = playerdb.T.drop_duplicates().T
playerdb.to_csv('./2017-18_NBA_Player_Statistics.csv')
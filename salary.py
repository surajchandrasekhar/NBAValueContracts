from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
html = urlopen('https://www.basketball-reference.com/contracts/players.html')
soup = BeautifulSoup(html, 'html.parser')
soup
events = soup.find_all("table")[0]
events
salaries = []
temp = []
i=0
contracts = events.find_all('tbody')
players = events.find_all('tr')
for player in players:
    numbers = player.find_all('td')
    for number in numbers:
        if(i%10 in [0,1,2]):
            temp.append(number.string)
        if(len(temp)==3):
            salaries.append(temp)
            temp = []
        i = i + 1
columns = ['Player', 'Team', 'Salary']
playersalaries = pd.DataFrame(salaries, columns=columns)
playersalaries.to_csv('./2018_19_NBA_Salaries.csv')
        
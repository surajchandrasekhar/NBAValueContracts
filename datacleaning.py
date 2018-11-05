#import packages
import pandas as pd
import numpy as np
#read datasets in 
players = pd.read_csv('2017-18_NBA_Player_Statistics.csv')
salaries = pd.read_csv('2018_19_NBA_Salaries.csv')
#Get all the players that played on multiple teams
players['PlayerID'] = players['Unnamed: 0']
temp=players[players['Tm']=='TOT']
#get list of player ids of players that played on more than one team
tempnums = np.array(temp['PlayerID'])
removes = []
for i in tempnums:
    removes.append(i)
    removes.append(i+1)
    removes.append(i+2)
#remove players that played on multiple teams
for i in range(len(players)):
    if(i in removes):
        players=players.drop(players['PlayerID'][i])
#add back players that played on multiple teams so that there is only one entry per player
players=pd.concat([players, temp])
players = players.sort_values(by='PlayerID')
#drop certain features from the Player table
players = players.drop(['Unnamed: 0', 'Tm'], axis=1)
#combine information on player stats and salary information
total = pd.merge(players, salaries, on='Player', how='inner')
#write as a csv file
total.to_csv('./PlayerSalaries.csv')

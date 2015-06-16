#!/usr/bin python
import requests
from bs4 import BeautifulSoup
import mysql.connector

###DATABASE CONNECT###

db = mysql.connector.connect(host="localhost",
                     user="root",
                      passwd="password",
                      db="nameofdatabase")

###/DATABASE CONNECT/###

###DATABASE QUERY###

c = db.cursor()

def nhl_data(team1, team2, score1, score2, time):
    c.execute("INSERT INTO nhl (team1, team2, score1, score2, time) VALUES (%s,%s,%s,%s,%s)",
              (team1, team2, score1, score2, time))
    db.commit()


def clear_nhl():
    c.execute("Truncate table nhl")

###/DATABASE QUERY/###

url = 'http://scores.espn.go.com/nhl/scoreboard'
r = requests.get(url)
soup = BeautifulSoup(r.text)  # entire page content

match_up = soup.find_all('table', {'class': 'game-header-table'})
team_scores = soup.find_all('table', {'class': 'game-header-table'})
game_info = soup.find_all('ul', {'class': 'game-info'})

team_match = []
scores = []
time = []

for score in team_scores:
    this_score = score.find_all('td', {'class': 'team-score'})
    for goals in this_score:
        scores.append(goals.contents[0].text)

for team in match_up:
    name = team.find_all('td', {'class': 'team-name'})
    for text in name:
        team_name = text.find_all('a')
        if text.contents[0].text != u'\xa0':
            team_match.append(text.contents[0].text)

for game_time in game_info:
    lis = game_time.contents[1]


for g in game_info:
    lis = g.find_all('li')
    for t in g:
        time.append(g.contents[0].text)

if len(scores) < len(team_match):
    while len(scores) < len(team_match):
        scores.append(0)

clear_nhl()

nhl_data("fill", "fill", "fill", "fill", "fill")

i = 0
while(i < len(team_match)-1):
    nhl_data(team_match[2*i], team_match[2*i+1], scores[2*i], scores[2*i+1], time[2*i])
    i += 1


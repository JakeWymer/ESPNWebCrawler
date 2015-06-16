#!/usr/bin/ python
__author__ = 'Jakey'
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector


###DATABASE CONNECT###

db = mysql.connector.connect(host="localhost",
                     user="root",
                      passwd="password",
                      db="nameofdatabase")

###/DATABASE CONNECT/###

###DATABASE QUERY###

c = db.cursor()

def mlb_data(team1, team2, score1, score2, time):
    c.execute("INSERT INTO mlb (team1, team2, score1, score2, time) VALUES (%s,%s,%s,%s,%s)",
              (team1, team2, score1, score2, time))
    db.commit()


def clear_mlb():
    c.execute("Truncate table mlb")

###/DATABASE QUERY/###

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get("http://scores.espn.go.com/mlb/scoreboard")
cont = driver.page_source

soup = BeautifulSoup(cont)

driver.quit()

match_up = soup.find_all('tbody', {'id': 'teams'})
runs = soup.find_all('td', {'class': 'total'})
time = soup.find_all('th', {'class': 'date-time'})


team_match = []
scores = []
inning = []

for team in match_up:
    names = team.find_all('h2')
    for n in names:
        t = n.find_all('a', {'name': '&lpos=mlb:scoreboard:team'})
        for match in t:
            team_match.append(match.text)

for run in runs:
    scores.append(run.text)

if len(scores) < len(team_match):
    while len(scores) < len(team_match):
        scores.append(0)

for inn in time:
    if inn.find('span'):
        a = inn.find_all('span', {'class': 'time'})
        for b in a:
            inning.append(b.text)
            inning.append('\n')
    else:
        inning.append(inn.text)
        inning.append('\n')


clear_mlb()

mlb_data("fill", "fill", "fill", "fill", "fill")

i = 0
while(i < len(team_match)):
    mlb_data(team_match[2*i], team_match[2*i+1], scores[2*i], scores[2*i+1], inning[2*i])
    i += 1


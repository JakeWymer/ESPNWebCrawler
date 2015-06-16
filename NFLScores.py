import requests
from bs4 import BeautifulSoup


url = 'http://scores.espn.go.com/nfl/scoreboard'
r = requests.get(url)
soup = BeautifulSoup(r.content)

match_up = soup.find_all('div', {'class': 'team visitor'})
team_scores = soup.find_all('ul', {'class': 'score'})
game_status = soup.find_all('div', {'class': 'game-status'})

team_match = []
scores = []
time = []


for team in match_up:
        team_match.append(team.contents[0].text)

for score in team_scores:
    if score.contents[5].text != 'T':
        scores.append(score.contents[5].text)

for status in game_status:
    time.append(status.contents[0].text)

print(team_match)
#print(scores)
#print(time)
# Specify thread IDs to scrape (the value after '?tid=' in a forum thread)
# threads = [29264, 29033, 29111,]
threads = []

# Specify either a list of users or a team
# If specifying a list of users, follow the below format
# If multiple users are specified, they should be on the same team according to the tracker
# users = ['Maglubiyet', 'Hordle', '']
users = []

# If specifying a team, please use the following abbreviations and format
# ISFL = AUS / AZ / BAL / BER / CHI / COL / HON / NO / NY / OCO / PHI / SAR / SJS / YKW
# DSFL = BBB / DAL / KC / LDN / MINN / NOR / POR / TIJ
# team = ['CHI']
team = []

########################################################################################################################
# DO NOT EDIT ANYTHING BELOW THIS LINE
########################################################################################################################
import datetime, json, re, requests, urllib.request
from bs4 import BeautifulSoup

# Map team abbreviations to JSON format along with weekly training thread IDs
teams_dict = {
    'AUS': ['AUSTIN_COPPERHEADS', 13404],
    'AZ': ['ARIZONA_OUTLAWS', 53],
    'BAL': ['BALTIMORE_HAWKS', 54],
    'BER': ['BERLIN_FIRE_SALAMANDERS', 25694],
    'CHI': ['CHICAGO_BUTCHERS', 13831],
    'COL': ['COLORADO_YETI', 51],
    'HON': ['HONOLULU_HAHALUA', 20472],
    'NO': ['NEW_ORLEANS_SECOND_LINE', 2034],
    'NY': ['NEW_YORK_SILVERBACKS', 25693],
    'OCO': ['ORANGE_COUNTY_OTTERS', 50],
    'PHI': ['PHILADELPHIA_LIBERTY', 2035],
    'SAR': ['SARASOTA_SAILFISH', 20473],
    'SJS': ['SAN_JOSE_SABERCATS', 49],
    'YKW': ['YELLOWKNIFE_WRAITHS', 52],
    'BBB': ['BONDI_BEACH_BUCCANEERS', 12670],
    'DAL': ['DALLAS_BIRDDOGS', 19293],
    'KC': ['KANSAS_CITY_COYOTES', 5409],
    'LDN': ['LONDON_ROYALS', 19292],
    'MINN': ['MINNESOTA_GREY_DUCKS', 5412],
    'NOR': ['NORFOLK_SEAWOLVES', 12722],
    'POR': ['PORTLAND_PYTHONS', 5410],
    'TIJ': ['TIJUANA_LUCHADORES', 5413],
}

# Throw error if no inputs are entered
if users == [] and team == []:
    raise ValueError('Please enter valid inputs for either the users or team fields.')

# Throw error for bad team value
if team != [] and team[0] not in teams_dict:
    raise ValueError('The format for the team name is invalid. Please try again.')

# Import team data from tracker if specified
if team != []:
    with urllib.request.urlopen('https://tracker.sim-football.com/players_json') as players_json:
        data = json.loads(players_json.read().decode())
    users.extend([x['user'] for x in data if x['team'] == teams_dict[team[0].upper()][0]])

# Sorting guarantees that TPE opportunities are displayed from oldest to newest
threads.sort()

# Initialize TPE and user dictionaries
user_TPE = {}
for user in users:
    user_TPE[user] = {}
    user_TPE[user]['threads'] = []
thread_users = {}
for thread in threads:
    thread_users[thread] = {}

# Let the scraping commence
for thread in threads:
    URL = 'https://forums.sim-football.com/showthread.php?tid=' + str(thread)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    page_title = soup.select("title")[0].get_text()
    thread_users[thread]['name'] = page_title + ", " + URL
    page_text = soup.find_all(class_="pages")[0].get_text()
    # Scraper only parses 10 posts at a time, so pages must be indexed
    pages = re.search('\((.*)\)', page_text).group(1)
    sub_users = []
    for num_pages in range(1, int(pages)):
        indexed_URL = URL + '&page=' + str(num_pages)
        page = requests.get(indexed_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        for x in range(0, 10):
            text_only = soup.find_all(class_="post_author scaleimages")[x].get_text()
            sub_users.append(text_only[1:text_only.find(" \n")])
    thread_users[thread]['users'] = sub_users

# Add TPE opportunity to user's entry if they have NOT posted
# This can be reversed if desired by removing the 'not' clause below
for dict in thread_users:
    for user in users:
        if user not in thread_users[dict]['users']:
            user_TPE[user]['threads'].append(thread_users[dict]['name'])

# Below code is specific to Weekly Training thread
# Date/time measurements needed for determining weekly training dates
today = datetime.date.today()
sunday = today - datetime.timedelta(days = today.weekday() + 1)
sunday = datetime.datetime.strptime(str(sunday), '%Y-%m-%d').strftime('%m-%d-%Y')

last_week_users = []
post_date = ''
if team != []:
    tid = teams_dict[team[0]][1]

# If no team was specified, find the first user's team
if team == []:
    with urllib.request.urlopen('https://tracker.sim-football.com/players_json') as players_json:
        data = json.loads(players_json.read().decode())
    team = (x['team'] for x in data if x['user'] == users[0])
    team = list(team)[0]
for item in teams_dict.values():
    if item[0] == team:
        tid = item[1]

URL = 'https://forums.sim-football.com/showthread.php?tid=' + str(tid)
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

page_text = soup.find_all(class_="pages")[0].get_text()
pages = re.search('\((.*)\)', page_text).group(1)
current_user = ''

# Append users who have posted since the start of the league week
for num_pages in reversed(range(1, int(pages))):
    indexed_URL = URL + '&page=' + str(num_pages + 1)
    page = requests.get(indexed_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    for x in reversed(range(0, len(soup.find_all(class_="post_author scaleimages")))):
        current_user = soup.find_all(class_="post_author scaleimages")[x].get_text()
        last_week_users.append(current_user[1:current_user.find(" \n")])
        post_date = soup.find_all(class_="post_date")[x]
        if sunday in str(post_date):
            break
    else:
        continue
    break

for user in users:
    if user not in last_week_users:
        user_TPE[user]['threads'].append('Weekly Training, ' + URL)

print(json.dumps(user_TPE, indent = 4))
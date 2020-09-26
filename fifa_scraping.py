import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
from players import FIFAPlayer, PlayerDatabase, create_FIFA_player

URL = 'https://www.futwiz.com/en/fifa20/career-mode/hidden-gems'


def get_fifa_gems_from_futwiz(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    players_table = soup.find("table", class_="table results playersearchresults")
    # print(players_table)
    players_rows = soup.find_all("tr", class_="table-row")
    print(players_rows[0])
    for player_row in players_rows:
        name_tag = player_row.find("p", class_="name").select("a > b")[0]
        name = name_tag.get_text()
        # print(name)
        # print(name_tag[0].get_text())
        stats = player_row.find_all("td", class_="statCol")
        # print(stats)
        stats_numbers = []
        for stat in stats:
            try:
                number = stat.select("div > div")[0].get_text()
            except Exception as excp:
                number = stat.get_text()
            if '\n' in number:
                _, number, _ = number.split('\n')
            # ['70', '86', '\nRM\n', '16', '\n17\n', '\n2022\n']
            stats_numbers.append(number)
        # stats_numbers = stats.select("div > div")
        # print(stats_numbers)
        [overall, potential, position, _ , age, contract_until] = stats_numbers
        player_attributes = {
            'name': name,
            'age': int(age),
            'position': position,
            'overall': int(overall),
            'potential': int(potential),
            'contract_until': int(contract_until),
        }
        create_FIFA_player(player_attributes)
        # print(new_player)

# option = Options()
# option.headless = True
# driver = webdriver.Firefox(options=option)

# driver.get(URL)

# driver.quit()

def retrieve_FIFA_gems_from_pages(page_limit: int):
    for idx in range(page_limit):
        url = f'https://www.futwiz.com/en/fifa20/career-mode/hidden-gems?page={idx}'
        get_fifa_gems_from_futwiz(url)


def store_FIFA_players_on_json():
    all_players = (PlayerDatabase.goalkeepers + PlayerDatabase.defenders + PlayerDatabase.midfielders + PlayerDatabase.attackers)
    with open('players.json', 'w') as file:
        json.dump([player.__dict__ for player in all_players], file, indent=4)


# Read JSON file
def get_data_from_json():
    with open('players.json') as data_file:
        data_loaded = json.load(data_file)
    return data_loaded


def populate_FIFA_players():
    data_loaded = get_data_from_json()
    for data in data_loaded:
        print(data)
        create_FIFA_player(data)


def filter_and_save_FIFA_players_on_json():
    filtered_players = PlayerDatabase.filter_players(PlayerDatabase.attackers, overall__lt=67, growth__gte=10)
    print(filtered_players)
    with open('filtered_players.json', 'w') as file:
        dumped_players = [player.__dict__ for player in filtered_players]
        json.dump(dumped_players, file, indent=4)

# url = f'https://www.futwiz.com/en/fifa20/career-mode/hidden-gems?page=0'
# get_fifa_gems_from_futwiz(url)

# RETRIEVING AND SAVING
# retrieve_FIFA_gems_from_pages(5)
# print(PlayerDatabase.players_amount)
# store_FIFA_players_on_json()

# RESTORING AND QUERYING
populate_FIFA_players()
filter_and_save_FIFA_players_on_json()
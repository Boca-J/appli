# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import requests

SPORT = 'soccer'  # Adjust after confirming the actual sport_key from the /sports endpoint

# Include all specified regions if the API does not support a wildcard for all regions
REGIONS = 'uk,us,eu,au'  # Adjust based on the API documentation if a wildcard or similar feature is available

# Keep other parameters as they are or adjust based on your requirements
MARKETS = 'h2h'  # Example: head-to-head and spreads
ODDS_FORMAT = 'decimal'  # Assuming decimal format is preferred
DATE_FORMAT = 'iso'  # ISO date format
API_KEY = "6f7597f8fe6386801a144d50b9400ae4"


def remove_space(text):
    return text.replace(" ", "_")

# Function to get the JSON data from the API endpoint
def get_china_data(url):
    response = requests.get(url)
    return response.json()


def get_usa_data():
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(
            f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        return odds_json

        # print('Number of events:', len(odds_json))
        # print(odds_json)
        #
        # # Check the usage quota
        # print('Remaining requests',
        #       odds_response.headers['x-requests-remaining'])
        # print('Used requests', odds_response.headers['x-requests-used'])

def parse_json_usa(usa_data, matches_data, name_dict):
    counter = 0
    for match in usa_data:
        home = match["home_team"]
        away = match["away_team"]

        odds_a = [-1.0, ""]
        odds_d = [-1.0, ""]
        odds_h = [-1.0, ""]

        for web_odd in match["bookmakers"]:
            # print(type(web_odd['markets'][0]))
            # print(web_odd)

            # exit()

            website = web_odd["key"]
            if odds_a[0] < float(web_odd['markets'][0]['outcomes'][0]['price']):
                odds_a[0] = float(web_odd['markets'][0]['outcomes'][0]['price'])
                odds_a[1] = website

            if odds_d[0] < float(web_odd['markets'][0]['outcomes'][2]['price']):
                odds_d[0] = float(web_odd['markets'][0]['outcomes'][2]['price'])
                odds_d[1] = website

            if odds_h[0] < float(web_odd['markets'][0]['outcomes'][1]['price']):
                odds_h[0] = float(web_odd['markets'][0]['outcomes'][1]['price'])
                odds_h[1] = website

        usa_odds = [odds_a, odds_d, odds_h]
        print(home)
        print(away)

        if home in name_dict:
            print("yes")
        else:
            print("no")

        if home in name_dict and away in name_dict:

            counter += 1
            team_code = (name_dict[home], name_dict[away])

            if team_code in matches_data:
                odds = matches_data[team_code]
                # odds will be [ odda,oddb, oddc]
                for i in range(len(odds)):
                    if usa_odds[i][0] > odds[i][0]:
                        odds[i][0] = usa_odds[i][0]
                        odds[i][1] = usa_odds[i][1]

                matches_data[team_code] = odds


            # only if none of the matches are matched
        else:

            team_code = (home, away)
            if team_code not in matches_data:
                matches_data[team_code] = usa_odds

            else:
                odds = matches_data[team_code]
                # odds will be [ odda,oddb, oddc]
                for i in range(len(odds)):
                    if usa_odds[i][0] > odds[i][0]:
                        odds[i][0] = usa_odds[i][0]
                        odds[i][1] = usa_odds[i][1]

                matches_data[team_code] = odds


def read_txt():

    filename = "name.txt"
    with open(filename, 'r') as file:
        processed_data = {}
        for line in file:
            if line.startswith('---'):  # Ignore lines after this
                continue

            # Split each line by comma, remove "队" from the Chinese name, and append to the list
            parts = line.split('-')
            if len(parts) == 2:
                english_name, chinese_name = parts
                if chinese_name[-2] == "队":
                    chinese_name = chinese_name[:-2]
                else:
                    chinese_name = chinese_name[:-1]

                processed_data[english_name] = chinese_name

            else:
                continue

    return processed_data









# Function to parse the JSON data from china website
def parse_json_china(json_data):
    matches_data = {}

    # Loop through each match info in the list
    for match_info in json_data["value"]["matchInfoList"]:
        for sub_match in match_info["subMatchList"]:
            # Extract the team codes and the had (Home/Away/Draw) odds
            home_name = sub_match["homeTeamAllName"]
            away_name = sub_match["awayTeamAllName"]

            if sub_match["had"] != {}:


                odds_a = float(sub_match["had"]["a"])
                odds_d = float(sub_match["had"]["d"])
                odds_h = float(sub_match["had"]["h"])

                # Create a tuple key of home and away team codes
                team_codes_key = (home_name, away_name)

                # Store the odds in a list and assign it to the dictionary with the team codes tuple as the key
                matches_data[team_codes_key] = [[ odds_a,"体彩",],[odds_d,"体彩"], [odds_h, "体彩"]]

    return matches_data

def find_odds(odds,profit):

    a = 100/odds[0][0]
    d = 100/odds[1][0]
    h = 100/odds[2][0]

    total_profit = 100 - a - d - h



    # for i in range(100):
    #     for j in range(100 - i):
    #         k = 100 - i - j
    #         min_profit = 0
    #
    #
    #         profit1 = i* odds[0][0]  - 100
    #         if profit1 > min_profit:
    #             min_profit = profit1
    #
    #
    #         profit2 = j* odds[1][0]  - 100
    #         if profit2 < min_profit:
    #             min_profit = profit2
    #
    #
    #         profit3 = k* odds[2][0] - 100
    #         if profit3 < min_profit :
    #             min_profit = profit3
    #
    #         if min_profit > 5 and min_profit > total_profit:
    #             total_profit = min_profit
    #             a = i
    #             d = j
    #             h = k

    if total_profit < profit:
        return 0, 0, 0, 0
    else:
        return total_profit, [odds[0][0],a, odds[0][1]], [odds[1][0],d, odds[1][1]], [odds[2][0], h, odds[2][1]]

def find_matches(matches_data, profit):
    match_list = []
    for team in matches_data:
        odds = matches_data[team]
        total_profit, a, d, h = find_odds(odds, profit)
        if total_profit == 0:
            continue

        match_list.append({"home_name": team[0], "away_name": team[1], "profit":total_profit, "away_odds":a[0], "away":a[1], "away_web": a[2], "draw_adds":d[0], "draw": d[1],"draw_web": d[2], "home_odds": h[0], "home":h[1], "home_web": h[2]})

    return match_list







# Press the green button in the gutter to run the script.
def get_data(profit):


    # URL to get the JSON data
    china_url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchCalculatorV1.qry?poolCode=hhad,had&channel=c"

    name_dict = read_txt()
    china_json_data = get_china_data(china_url)


    # Parse the JSON data to extract the required information
    matches_data = parse_json_china(china_json_data)



    # print(matches_data)
    usa_json_data = get_usa_data()
    #
    parse_json_usa(usa_json_data, matches_data, name_dict)


    match_list = find_matches(matches_data,profit)

    # match_list = [[100, (2,0,20, "bein"),(1,9, 40,"体彩"), (2.5,40, 'footy')]]

    return match_list


if __name__ == "__main__":
    match_list = get_data(0)
    print(match_list)



    # # Get the JSON data from the API
    # json_data = get_china_data(china_url)

    #
    # # Parse the JSON data to extract the required information
    # china_matches_data = parse_json_china(json_data)


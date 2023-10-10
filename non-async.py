# This script is to scrape the entire web steam library to find games that add +1 to games owned counter
# SteamDB will not work as these games seem to be bugged and do not follow their actual tagged logic
#
# List of all +1 games seem to contain "Install Game" versus "Download" or "Add To Library"
# Serena
# http://store.steampowered.com/app/272060/
# Grimm (DLC 1)
# http://store.steampowered.com/app/261390/
# Portal 2 Sixense Perceptual Pack
# http://store.steampowered.com/app/247120/
# RACE 07: Andy Priaulx Crowne Plaza Raceway (Free DLC)
# http://store.steampowered.com/app/8650/
# Penumbra: Necrologue
# http://store.steampowered.com/app/346290/
# The Descendant
# http://store.steampowered.com/app/351940/
# Romance of the Three Kingdoms Maker / 三国志ツクール
# http://store.steampowered.com/app/397720/
# Amnesia: Final Revelations
# http://store.steampowered.com/app/508380/
#
# TODO Gather all steam apps IDs these can easily be incremented by 10 every single time Scrape the webpage and see
#  if it contains the text "Install Game" and simply put the result with APPID and true/false into .txt file Detect
#  last appid ran in the text file and resume the program from that point Detect steam's web API limit before being
#  banned and giving invalid results
import concurrent.futures
import urllib.request  # https://docs.python.org/3/library/urllib.request.html
import os


def resumeprogress():
    if os.path.exists("searched.txt"):
        print("Found existing search file")
        with open('searched.txt', 'r') as file_data:
            for line in file_data:
                pass
            last_line = line
        print(f"Found last progress line: {last_line}")
        return int(last_line.split(",")[0])
    else:
        print("could not find existing file")
        return 0


def saveprogress(app_id, app_result, app_name):
    with open('searched.txt', 'a') as outputfile:
        outputfile.write(f"{app_id},{app_result},{app_name}\n")


def steamscraping(appid):
    try:
        steam_grab_rawpage = urllib.request.urlopen(f"https://store.steampowered.com/app/{appid}/")
        # print(f"---Result---\n{steam_grab_rawpage}")
        steam_html_page = steam_grab_rawpage.read().decode()
        # print(f"---HTML VERSION---\n{steam_html_page}")
        steam_html_title = steam_html_page.split('<title>')[1].split('</title>')[0]
        print(f"ID:{appid} {steam_html_title}")

        if steam_html_title == 'Welcome to Steam':
            print("Invalid game, go next!")
            saveprogress(appid, 0, 0)
            return 0
        if 'Install Game' in steam_html_page:
            print("We found a game!")
            saveprogress(appid, 9999, steam_html_title.replace(' on Steam', ''))
            return 0
        else:
            print("No game found, go next!")
            saveprogress(appid, 0, steam_html_title.replace(' on Steam', ''))
            return 0
    except urllib.error.HTTPError as e:
        print(f"error occurred loading appid {appid}: {e}")

        if e.code == 302:
            print("Redirect error loop avoided!")
            saveprogress(appid, 0, "REDIRECT ERROR AVOIDED")
            return 0
        else:
            return -1


if __name__ == "__main__":
    #Note: limit is http request speed, maybe
    current_appid = resumeprogress()
    #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    while True:
        current_appid += 10
        result = steamscraping(current_appid)
        #result = executor.submit(steamscraping, current_appid).result()

        if result == -1:
            break
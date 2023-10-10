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
# TODO
#  - Gather all steam apps IDs these can easily be incremented by 10 every single time Scrape the webpage
#  - See if it contains the text "Install Game" and simply put the result with APPID and true/false into .txt file
#  - Detect last appid ran in the text file and resume the program from that point Detect steam's web API limit before
#  being banned and giving invalid results
import asyncio  # https://realpython.com/async-io-python/
import httpx  # https://www.python-httpx.org/quickstart/
import urllib.request  # https://docs.python.org/3/library/urllib.request.html
import os


async def resumeprogress():
    if os.path.exists("searched.txt"):
        print("Found existing search file")
        with open('searched.txt', 'r', encoding='utf-8') as file_data:
            for line in file_data:
                pass
            last_line = line
        print(f"Found last progress line: {last_line}")
        return int(last_line.split(",")[0])
    else:
        print("could not find existing file")
        return 0


async def saveprogress(app_id, app_result, app_name):
    with open('searched.txt', 'a', encoding='utf-8') as outputfile:
        outputfile.write(f"{app_id},{app_result},{app_name}\n")


async def steamscraping(appid):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://store.steampowered.com/app/{appid}/")
            response.raise_for_status()

            steam_html_page = response.text
            steam_html_title = steam_html_page.split('<title>')[1].split('</title>')[0]
            print(f"ID:{appid} {steam_html_title}")

            if steam_html_title == 'Welcome to Steam' or response.is_redirect:  # This is kind of useless now since moving to httpx
                print("Invalid game, go next!")
                await saveprogress(appid, 0, 0)
                return 0
            if 'Install Game' in steam_html_page:  # Should give a +1 game unless it was public and patched
                print("We found a game!")
                await saveprogress(appid, 9999, steam_html_title.replace(' on Steam', ''))
                return 0
            else:
                print("No game found, go next!")
                await saveprogress(appid, 0, steam_html_title.replace(' on Steam', ''))
                return 0
    except httpx.HTTPError as e:
        if e.response.status_code == 302:  # Catch if the page is redirected
            print(f"ID:{appid}, redirected")
            await saveprogress(appid, 0, 0)
            return 0
        else:  # Haven't hit this yet besides a 502 error a really weird 505
            print(f"Error occurred loading appid {appid}: {e}")
            return -1


async def main():
    current_appid = await resumeprogress()

    async with httpx.AsyncClient() as client:
        while True:
            current_appid += 10
            result = await steamscraping(current_appid)

            if result == -1:
                break


if __name__ == "__main__":
    asyncio.run(main())

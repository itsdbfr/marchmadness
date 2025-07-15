from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

import random
import time
import pandas as pd
import openpyxl

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

randomSleep = random.randint(1, 4)

url = "https://stats.ncaa.org/active_career_leaders/view_rankings?id=2916608"
driver.get(url)

time.sleep(randomSleep)

resultsDisplayedButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[5]/div/div[2]/label/select')
resultsDisplayedButton.click()

maxResultsButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[5]/div/div[2]/label/select/option[4]')
maxResultsButton.click()

time.sleep(randomSleep)

rankList = []
playerList = []
teamList = []
divList = []
pointsList = []
threePointsList = []
averagePointsList = []
gamesPlayedList = []
yearList = []

aggregatedData = []

season = 1
year = 2023



while season <= 1:
    
    seasonDisplayedButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/nav/div/ul/li[2]/a')
    seasonDisplayedButton.click()

    seasonSelect = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[1]/nav/div/ul/li[2]/div/a[{season}]')
    seasonSelect.click()

    time.sleep(randomSleep)

    i = 1
    page = 1

    while page != 3:
        try:
            # Retry mechanism for stale elements
            retry_attempts = 3
            for attempt in range(retry_attempts):
                try:
                    rank = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[1]')
                    player = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[2]/a[1]')
                    team = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[2]/a[2]')
                    div = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[3]')
                    points = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[11]')
                    threePoints = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[9]')
                    averagePoints = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[12]')
                    gamesPlayed = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div[5]/div/table/tbody/tr[{i}]/td[7]')
                    
                    # Append data
                    rankList.append(rank.text)
                    playerList.append(player.text)
                    teamList.append(team.text)
                    divList.append(div.text)
                    pointsList.append(points.text)
                    threePointsList.append(threePoints.text)
                    averagePointsList.append(averagePoints.text)
                    gamesPlayedList.append(gamesPlayed.text)
                    yearList.append(str(year))
                    

                    break  # If no exception, break retry loop
                
                except StaleElementReferenceException:
                    if attempt == retry_attempts - 1:
                        print(f"Skipping row {i} on page {page} due to repeated stale element issues.")

        except Exception as e:
            print(f"Error on page {page}, row {i}: {e}")
        
        i += 1

        if i == 101:
            nextPageButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[5]/div/div[6]/a[2]')
            nextPageButton.click()
            time.sleep(randomSleep)
            i = 1
            page += 1
            
    
    firstPageButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[5]/div/div[6]/span/a[1]')
    firstPageButton.click()
    
    time.sleep(randomSleep)
    
    season += 1
    year -= 1

driver.quit()

for year, rank, player, team, div, points, threePoints, averagePoints, gamesPlayed in zip(yearList, rankList, playerList, teamList, divList, pointsList, threePointsList, averagePointsList, gamesPlayedList):
    row = [year, rank, player, team, div, points, threePoints, averagePoints, gamesPlayed]
    aggregatedData.append(row)

ballDf = pd.DataFrame(aggregatedData, columns=['Year', 'Rank', 'Name', 'Team', 'Division', 'Points Scored', 'Three Pointers Scored', 'Average Points Scored', 'Games Played'])
fileLocation = '/Users/db/Desktop/Fordham/March Madness/Python/TopScorerData2025.xlsx'
ballDf.to_excel(fileLocation, index=False)

print(f"Scraping completed. Data saved to {fileLocation}.")

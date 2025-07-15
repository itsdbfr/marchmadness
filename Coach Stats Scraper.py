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

url = "https://stats.ncaa.org/head_coaches"
driver.get(url)
time.sleep(randomSleep)

filterButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[2]/div[2]')
filterButton.click()

time.sleep(1)

ballFilterButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[2]/div[2]/div/ul/li[3]')
ballFilterButton.click()

resultsDisplayedButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/label/select')
resultsDisplayedButton.click()

maxResultsButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[1]/label/select/option[2]')
maxResultsButton.click()

time.sleep(3)

coachList = []
seasonsList = []
tenureList = []
winsList = []
lossesList = []
winLossPercentageList = []
currentTeamList = []

aggregatedData = []

i = 1
page = 1

while page != 434:
    try:
        # Retry mechanism for stale elements
        retry_attempts = 3
        for attempt in range(retry_attempts):
            try:
                coachName = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[1]/a')
                totalSeasons = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[2]')
                totalWins = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[5]')
                totalLosses = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[6]')
                winLossPercent = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[8]')
                tenure = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[4]')

                try:
                    currentTeam = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/div/div/div/table/tbody/tr[{i}]/td[3]/a')
                    currentTeamList.append(currentTeam.text)
                except NoSuchElementException:
                    currentTeamList.append("Retired")

                # Append data
                coachList.append(coachName.text)
                seasonsList.append(totalSeasons.text)
                winsList.append(totalWins.text)
                lossesList.append(totalLosses.text)
                winLossPercentageList.append(winLossPercent.text)
                tenureList.append(tenure.text)

                break  # If no exception, break retry loop
            except StaleElementReferenceException:
                if attempt == retry_attempts - 1:
                    print(f"Skipping row {i} on page {page} due to repeated stale element issues.")

    except Exception as e:
        print(f"Error on page {page}, row {i}: {e}")

    i += 1

    if i == 26:
        nextPageButton = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[5]/a[3]')
        nextPageButton.click()
        time.sleep(2)
        i = 1
        page += 1

driver.quit()

for coach, season, win, loss, winLoss, tenure, team in zip(coachList, seasonsList, winsList, lossesList, winLossPercentageList, tenureList, currentTeamList):
    row = [coach, season, win, loss, winLoss, tenure, team]
    aggregatedData.append(row)

ballDf = pd.DataFrame(aggregatedData, columns=['Coach Name', 'Total Seasons', 'Total Wins', 'Total Losses', 'WL%', 'All Tenures', 'Current Team'])
fileLocation = '/Users/db/Desktop/Fordham/March Madness/Python/CoachData.xlsx'
ballDf.to_excel(fileLocation)

print(f"Scraping completed. Data saved to {fileLocation}.")

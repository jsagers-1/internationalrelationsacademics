## Project Members: Jacob Sagers, Zola Racklin, and Samara Shaz
## Code Description: The following code below includes a webscraper to dynamically scrape rankings from our first rankings website,
## and the unfinished code to crawl our second rankings data.
## AI USE: AI was used to help decipher coding error messages with Selenium.

## import necessary libraries
from bs4 import BeautifulSoup as bs 
import requests 
import pandas as pd
import re
import time
import selenium
from selenium import webdriver


def rankings_scraper(starting_url, filename):
    '''
    A rankings webpage scraper for Shanghai rankings. The function takes in rankings
    by subdiscipline and returns the univerisities' names, rank, and country. It also crawls
    every webpage to scrape the entire rankings.
    
    Inputs:
    starting_url: a url that links to the Shanghai University website page to be scraped.
    filname: the desired filename for the csv file represented as a string.

    Output: 
    a dataframe containing the list of dictionaries
    '''

    header = { "User-Agent" : "Practice Scraper for educational project @jsagers@uchicago.edu" } 
    ##create a list to store dictionaries
    univ_lst = []
    shanghai_response = requests.get(starting_url, headers = header)
    #check the requests code
    print("Our response code is:", shanghai_response.status_code)

    #use selenium's webdriver to scroll through the pages of interest.
    driver = webdriver.Chrome()

    try:
        driver.get(starting_url)
        # Give the initial page a moment to load
        time.sleep(1) 

        while True:
            ## turn the response into text and parse it with the bs library
            soup = bs(driver.page_source, "html.parser")

            ## find the broader frame that hosts each row.
            rows = soup.find_all("tr")
            #within the rows for each page, find the name, location, and ranking.
            for row in rows:
                number = row.find("div", {"class": "ranking"})
                name = row.find("span", {"class": "univ-name"})
                country = row.find("div", {"class" : "location"})

                #check to make sure the row is not empty, then strip
                if number and name and country:
                    rank = number.get_text(strip=True)
                    univ = name.get_text(strip=True)
                    coun = country.get_text(strip=True)
                    
                    #append each unique dictionary to the overall list using name and ranking as the key value pair with titles for the csv
                    univ_lst.append({"University": univ, "Country": coun, "Ranking": rank})

            ## initiate try to find the next page
            try:
                # find the next button element
                next_btn = driver.find_element("class name", "ant-pagination-next")
                
                #check if the button is disabled because last page has a special class
                button_class = next_btn.get_attribute("class")
                if "ant-pagination-disabled" in button_class:
                    break
                
                # if not, scroll to the next page using execute script and be respectful with time.
                driver.execute_script("arguments[0].scrollIntoView();", next_btn)
                time.sleep(2)
                next_btn.click()
            
            #stop if could not find the next button.
            except:
                break

    #ensure to finally quit the driver
    finally:
        driver.quit()
    
    #change into a dataframe and export to csv
    df = pd.DataFrame(univ_lst)
    df.to_csv(filename, index=False)

    return df


## run for each subdiscipline ranking
rankings_scraper("https://www.shanghairanking.com/rankings/gras/2024/AS0504", "poli_sci_rankings.csv")
rankings_scraper("https://www.shanghairanking.com/rankings/gras/2024/AS0505", "sosc_rankings.csv")
rankings_scraper("https://www.shanghairanking.com/rankings/gras/2024/AS0501", "econ_rankings.csv")





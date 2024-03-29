
## Imports


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
import time
import io
import pandas as pd
import numpy as np
import csv
import os  # For cloud
## function definition

def scrapfyt(url):
    
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')

    # Install ChromeDriver and get its path
    chromedriver_path = ChromeDriverManager().install()

    # Initialize Chrome WebDriver with options
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)


    # Load the URL and get the page source
    driver.implicitly_wait(6)

    time.sleep(1)
    driver.get(url)
    time.sleep(2)

    ## Pause youtube video

    pause = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))

    # Move to the element before clicking
    ActionChains(driver).move_to_element(pause).click().perform()

    time.sleep(2.2)

    # Move to the element before clicking again
    ActionChains(driver).move_to_element(pause).click().perform()

    time.sleep(4)

    ## Scrolling through all the comments

    # Initial Scroll
    driver.execute_script("window.scrollBy(0,500)","")
        
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down till "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(4)
        
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
          break
        last_height = new_height
        
    # One last scroll just in case
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    ## Scraping details

    ## title of video
    video_title = driver.find_element(By.NAME, 'title').get_attribute('content')

    ## owner of video
    video_owner1 = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
    video_owner = []
    for owner in video_owner1:
        video_owner.append(owner.text)
    video_owner = video_owner[0]

    # total comments with replies
    video_comment_with_replies = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[1]').text + ' Comments'

    ## Scraping all the comments
    users = driver.find_elements(By.XPATH, '//*[@id="author-text"]/yt-formatted-string')

    comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')



    with io.open('comments.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Username", "Comment"])
        for username, comment in zip(users, comments):
            writer.writerow([username.text, comment.text])
        
    commentsfile = pd.read_csv("comments.csv", encoding ="utf-16")  # , encoding ="utf-16", engine = 'python'

    all_comments = commentsfile.replace(np.nan, '-', regex = True)
    all_comments = all_comments.to_csv("Full_Comments.csv", index = False)
    # comments.to_html("Comments2.html")

    ##total comments without replies
    video_comment_without_replies = str(len(commentsfile.axes[0])) + ' Comments'

    
    print(video_title, video_owner, video_comment_with_replies, video_comment_without_replies)
    print("check 1")
    test = pd.read_csv("Full_Comments.csv") 
    print(test)

    ## Close driver

    driver.close()
 
    return all_comments, video_title, video_owner, video_comment_with_replies, video_comment_without_replies


#var = scrapfyt("https://www.youtube.com/watch?v=PzzDVPcToWo")



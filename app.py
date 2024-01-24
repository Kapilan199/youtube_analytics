from flask import Flask, render_template, request
# import web_scraping, comment_sentiment_analysis, send_mail, delete_files, data_visual
import pandas as pd
## Imports






import matplotlib.pyplot as plt
from io import BytesIO
import base64



def plot(positive_comments,negative_comments):

    # Data
    categories = ['Positive Comments', 'Negative Comments']
    counts = [positive_comments, negative_comments]

    # Plotting
    plt.bar(categories, counts, color=['green', 'red'])
    plt.xlabel('Sentiment')
    plt.ylabel('Number of Comments')
    plt.title('Sentiment Analysis of Comments')

    # Save plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    return base64.b64encode(image_stream.read()).decode('utf-8')




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

## Mail Sending function

def mailsend(emailto, encoded_image):

  ## Mail details
  emailfrom = "sentimentanalysiskr@gmail.com"
  fileToSend = ["Full_Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]
  username = "sentimentanalysiskr@gmail.com"
  password = "xylh djhb yfwp ckgu"

  ## Mail Subject

  msg = MIMEMultipart()
  msg["From"] = emailfrom
  msg["To"] = emailto
  msg["Subject"] = "Hi your youtube comments excel file and graphs are here   -Youtube Comment Scraper"
  # msg.preamble = "Hi your csv file is ready from  -Youtube Comment Scraper"

  ## Adding attachments

  subtype = 'vnd.ms-excel'  # Subtype for excel or csv files
  for f in fileToSend:
    fp = open(f, encoding = 'utf8')
    attachment = MIMEText(fp.read(), _subtype = subtype)
    fp.close()
    attachment.add_header("Content-Disposition", "attachment", filename=f)
    msg.attach(attachment)



    image_data = base64.b64decode(encoded_image)
    image_attachment = MIMEImage(image_data, name='image.png')
    image_attachment.add_header('Content-ID', '<inline-image>')
    msg.attach(image_attachment)

  ## Sending mail to the user

  server = smtplib.SMTP("smtp.gmail.com:587")
  server.starttls()
  server.login(username,password)
  server.sendmail(emailfrom, emailto, msg.as_string())
  server.quit()



























def file_delete():
    file_to_delete = ["0.csv", "1.csv", "comments.csv", "Full_Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]

    for f in file_to_delete:
        os.remove(f)










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

  pause = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))

# Move to the element before clicking
  ActionChains(driver).move_to_element(pause).click().perform()

  time.sleep(2.2)

# Move to the element before clicking again
  ActionChains(driver).move_to_element(pause).click().perform()

  time.sleep(4)

  # pause.click()
  # time.sleep(0.2)
  # pause.click()
  # time.sleep(4)

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
  test = pd.read_csv("Full_Comments.csv") 
  print(test)

  ## Close driver

  driver.close()
 
  # print("Scraping is finished")

  ## return fuction

  return all_comments, video_title, video_owner, video_comment_with_replies, video_comment_without_replies


#var = scrapfyt("https://www.youtube.com/watch?v=PzzDVPcToWo")

















































import pandas as pd
import csv
import nltk
import os.path as checkcsv
import ssl
# Download the vader_lexicon resource

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('vader_lexicon')


## Downloads

def sepposnegcom(comment_file):

    ## Reading Dataset

    dataset = pd.read_csv(comment_file, encoding_errors = 'ignore')
    dataset = dataset.iloc[:, 0:]

    ## Getting Full Comments to csv file

    # full_com = dataset
    # full_comments = full_com.to_csv("Full Comments.csv")

    ## Sentiment analysis of comments using vadar sentiment analyser

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)

        if scores["neg"] > scores["pos"]:
            return 0
        return 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x : vader_sentiment_result(x))

    ## Separating Positive and Negative Comments

    for (sentiment), group in dataset.groupby(['vader_sentiment']):
         group.to_csv(f'{sentiment}.csv', index=False)
    
    if checkcsv.exists('1.csv') == False:                             # If 1.csv file does not exist, it creates one empty 1.csv file.
        with open('1.csv', 'w', encoding='UTF8', newline='') as f1:
            writer1 = csv.writer(f1)
            header1 = ['Empty', 'Empty', 'Empty']
            row1 = ['No Positive Comments', 'No Positive Comments', 'No Positive Comments']
            writer1.writerow(header1)
            writer1.writerow(row1)

    if checkcsv.exists('0.csv') == False:                             # If 1.csv file does not exist, it creates one empty 1.csv file.
        with open('0.csv', 'w',encoding='UTF8', newline='') as f0:
            writer0 = csv.writer(f0)
            header0 = ['Empty', 'Empty', 'Empty']
            row0 = ['No Negative Comments', 'No Negative Comments', 'No Negative Comments']
            writer0.writerow(header0)
            writer0.writerow(row0)
    
    pos = (pd.read_csv("1.csv", engine = 'python')).iloc[:, :-1]
    neg = (pd.read_csv("0.csv", engine = 'python')).iloc[:, :-1]

    positive_comments = pos.to_csv("Positive_Comments.csv", index=False)
    negative_comments = neg.to_csv("Negative_Comments.csv",index=False)

    video_positive_comments = str(len(pos.axes[0])) + ' Comments'  #Finding total rows in positive comments
    video_negative_comments = str(len(neg.axes[0])) + ' Comments'  #Finding total rows in negative comments
    
    if (pd.read_csv('1.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_positive_comments = '0 Comments'
    if (pd.read_csv('0.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_negative_comments = '0 Comments'
    print("testing full comments")
    print(positive_comments, negative_comments, video_positive_comments, video_negative_comments)    

    ## return function
    return positive_comments, negative_comments, video_positive_comments, video_negative_comments






































app = Flask(__name__)













@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods = ['POST'])
def scrap_comments():
    url = request.form.get('youtube url')
    emailto = request.form.get('user mail id')

# 1. scrapes url and return file with comments and other details
    file_and_detail = scrapfyt(url)





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

    pause = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-play-button')))

    # Move to the element before clicking
    ActionChains(driver).move_to_element(pause).click().perform()

    time.sleep(2.2)

    # Move to the element before clicking again
    ActionChains(driver).move_to_element(pause).click().perform()

    time.sleep(4)

    # pause.click()
    # time.sleep(0.2)
    # pause.click()
    # time.sleep(4)

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


    file_and_detail = all_comments, video_title, video_owner, video_comment_with_replies, video_comment_without_replies































# 2. takes the files and analyzes it and return the list positive and negative comments and the number of each.
    # sentiment = sepposnegcom("Full_Comments.csv")


 ## Reading Dataset

    dataset = pd.read_csv("Full_Comments.csv", encoding_errors = 'ignore')
    print("check 2")
    print(dataset)
    dataset = dataset.iloc[:, 0:]

    ## Getting Full Comments to csv file

    # full_com = dataset
    # full_comments = full_com.to_csv("Full Comments.csv")

    ## Sentiment analysis of comments using vadar sentiment analyser

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)

        if scores["neg"] > scores["pos"]:
            return 0
        return 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x : vader_sentiment_result(x))

    ## Separating Positive and Negative Comments

    for (sentiment), group in dataset.groupby(['vader_sentiment']):
         group.to_csv(f'{sentiment}.csv', index=False)
    
    if checkcsv.exists('1.csv') == False:                             # If 1.csv file does not exist, it creates one empty 1.csv file.
        with open('1.csv', 'w', encoding='UTF8', newline='') as f1:
            writer1 = csv.writer(f1)
            header1 = ['Empty', 'Empty', 'Empty']
            row1 = ['No Positive Comments', 'No Positive Comments', 'No Positive Comments']
            writer1.writerow(header1)
            writer1.writerow(row1)

    if checkcsv.exists('0.csv') == False:                             # If 1.csv file does not exist, it creates one empty 1.csv file.
        with open('0.csv', 'w',encoding='UTF8', newline='') as f0:
            writer0 = csv.writer(f0)
            header0 = ['Empty', 'Empty', 'Empty']
            row0 = ['No Negative Comments', 'No Negative Comments', 'No Negative Comments']
            writer0.writerow(header0)
            writer0.writerow(row0)
    
    pos = (pd.read_csv("1.csv", engine = 'python')).iloc[:, :-1]
    neg = (pd.read_csv("0.csv", engine = 'python')).iloc[:, :-1]
     
    print("check 3")
    print(pos)

    positive_comments = pos.to_csv("Positive_Comments.csv", index=False)
    negative_comments = neg.to_csv("Negative_Comments.csv",index=False)

    print("check 4")
    print(positive_comments)

    video_positive_comments = str(len(pos.axes[0])) + ' Comments'  #Finding total rows in positive comments
    video_negative_comments = str(len(neg.axes[0])) + ' Comments'  #Finding total rows in negative comments
    
    if (pd.read_csv('1.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_positive_comments = '0 Comments'
    if (pd.read_csv('0.csv', nrows=0).columns.tolist())[0] == 'Empty':
        video_negative_comments = '0 Comments'
    print("testing full comments")
    print(positive_comments, negative_comments, video_positive_comments, video_negative_comments)    

    ## return function
    sentiment = positive_comments, negative_comments, video_positive_comments, video_negative_comments
























































# 3. converting to list and formating
    list_file_and_detail = list(file_and_detail)
    list_sentiment = list(sentiment)
    print(list_file_and_detail)
    video_title, video_owner, video_comment_with_replies, video_comment_without_replies = list_file_and_detail[1:]
    pos_comments_csv, neg_comments_csv, video_posive_comments, video_negative_comments = list_sentiment
    pos_comments_csv = pd.read_csv('Positive_Comments.csv')
    neg_comments_csv = pd.read_csv('Negative_Comments.csv')
    print("File checking contents:")
    print(list_sentiment)
    print("File checking contents:")


    numeric_part = ''.join(filter(str.isdigit, video_posive_comments))
    # Convert the numeric part to an integer
    positive_number = int(numeric_part)
    numeric_part = ''.join(filter(str.isdigit, video_negative_comments))
    # Convert the numeric part to an integer
    negative_number = int(numeric_part)

    encoded_image = plot(positive_number, negative_number)
    # Render template with the encoded image


# 4. send the csv created by the sentiment file to the given email id
    # mailsend(emailto, encoded_image)

    emailfrom = "sentimentanalysiskr@gmail.com"
    fileToSend = ["Full_Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]
    username = "sentimentanalysiskr@gmail.com"
    password = "xylh djhb yfwp ckgu"

    ## Mail Subject

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Hi your youtube comments excel file and graphs are here   -Youtube Comment Scraper"
    # msg.preamble = "Hi your csv file is ready from  -Youtube Comment Scraper"

    ## Adding attachments

    subtype = 'vnd.ms-excel'  # Subtype for excel or csv files
    for f in fileToSend:
        fp = open(f, encoding = 'utf8')
        attachment = MIMEText(fp.read(), _subtype = subtype)
        fp.close()
        attachment.add_header("Content-Disposition", "attachment", filename=f)
        msg.attach(attachment)



        image_data = base64.b64decode(encoded_image)
        image_attachment = MIMEImage(image_data, name='image.png')
        image_attachment.add_header('Content-ID', '<inline-image>')
        msg.attach(image_attachment)

    ## Sending mail to the user

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()



#  5. delete the comment files because we dont need them anymore
    # file_delete()
    file_to_delete = ["0.csv", "1.csv", "comments.csv", "Full_Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]

    for f in file_to_delete:
        os.remove(f)

    after_complete_message = "Your file is ready and sent to your mail id"


  


    return render_template("index.html",after_complete_message = after_complete_message, title = video_title,
                           owner = video_owner, comment_w_replies = video_comment_with_replies,
                           comment_wo_replies = video_comment_without_replies,
                           positive_comment = video_posive_comments, negative_comment = video_negative_comments,
                           pos_comments_csv = [pos_comments_csv.to_html()], neg_comments_csv = [neg_comments_csv.to_html()],encoded_image=encoded_image)

# if __name__ == "app":
#     app.run()
@app.route('/test')
def test():
    with open("test.txt", 'w') as f:
        f.write("test")
    with open("test.txt", 'r') as f:
        c = f.readlines()
    return c

@app.route('/testt')
def testt():
    # Create a CSV file
    data = {'Name': ['John', 'Jane', 'Bob'], 'Age': [25, 30, 22]}
    df = pd.DataFrame(data)
    df.to_csv('test.csv', index=False)

    # Read the CSV file
    read_df = pd.read_csv('test.csv')

    # Return the content of the CSV file
    print(read_df)
    return read_df.to_html()
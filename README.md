# YouTube Comment Sentiment Analyzer

## Project Overview

This project is a YouTube comment sentiment analyzer that utilizes Selenium for scraping YouTube comments, NLTK's VADER sentiment analysis tool for sentiment analysis, and Matplotlib for data visualization. The goal is to analyze the sentiment of comments on YouTube videos and present the results through CSV files, a Matplotlib graph, and an HTML webpage.

## Features

1. **YouTube Comment Scraping:**
   - The project uses Selenium to scrape comments from YouTube videos. It navigates through the video pages, extracts comments, and stores them for analysis.

2. **Sentiment Analysis:**
   - The NLTK library is employed for sentiment analysis. The SentimentIntensityAnalyzer from NLTK's VADER module is used to assign sentiment scores to each comment.

3. **Filtering Positive and Negative Comments:**
   - Comments are filtered based on their sentiment scores. Positive and negative comments are segregated for further analysis.

4. **CSV File Creation:**
   - The project generates CSV files containing information about the comments, including the comment text, sentiment scores, and other relevant details.

5. **Matplotlib Graph:**
   - Matplotlib is used to create a graphical representation of the sentiment scores. The graph provides a visual overview of the distribution of positive and negative comments.

6. **HTML Webpage Display:**
   - The CSV files and Matplotlib graph are integrated into an HTML webpage. Users can view the sentiment analysis results in a user-friendly format.

7. **Email Notification:**
   - The project allows users to enter their email address. Once the sentiment analysis is complete, all CSV files, the Matplotlib graph, and the HTML webpage are sent to the specified email address.

## Images


## Usage

1. **Setup:**
   - Install the required libraries using `pip install selenium nltk matplotlib`.

2. **Run the Script:**
   - Execute the script to initiate the YouTube comment scraping, sentiment analysis, and file generation.

3. **Enter Email Address:**
   - Provide the email address where you want to receive the analysis results.

4. **Access Results:**
   - Once the analysis is complete, check your email for the CSV files, Matplotlib graph, and a link to the HTML webpage.

## Main Dependencies

- Selenium
- NLTK
- Matplotlib
- smtplib


## Note

Ensure that you comply with YouTube's terms of service and guidelines while using this tool. Unauthorized scraping or misuse of data may violate YouTube's policies.

Feel free to explore and enhance the project further according to your needs.

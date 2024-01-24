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
    print("check 2")
    print(dataset)
    dataset = dataset.iloc[:, 0:]

    ## Sentiment analysis of comments using vadar sentiment analyser

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    analyser = SentimentIntensityAnalyzer()

    def vader_sentiment_result(sent):
        scores = analyser.polarity_scores(sent)

        if scores["neg"] > scores["pos"]:
            return 0
        return 1

    dataset['vader_sentiment'] = dataset['Comment'].apply(lambda x : vader_sentiment_result(x))
    print("checking 1")
    print(dataset)
    ## Separating Positive and Negative Comments

    positive_comments = dataset[dataset['vader_sentiment'] == 1]
    negative_comments = dataset[dataset['vader_sentiment'] == 0]

    positive_comments.to_csv("Positive_Comments.csv", index=False)
    negative_comments.to_csv("Negative_Comments.csv", index=False)

    print("check 4")
    print(positive_comments)

    video_positive_comments = str(len(positive_comments)) + ' Comments'  #Finding total rows in positive comments
    video_negative_comments = str(len(negative_comments)) + ' Comments'  #Finding total rows in negative comments
    
    print("testing full comments")
    print(positive_comments, negative_comments, video_positive_comments, video_negative_comments)    

    ## return function
    return positive_comments, negative_comments, video_positive_comments, video_negative_comments









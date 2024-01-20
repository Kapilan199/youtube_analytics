from flask import Flask, render_template, request
import web_scraping, comment_sentiment_analysis, send_mail, delete_files
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods = ['POST'])
def scrap_comments():
    url = request.form.get('youtube url')
    emailto = request.form.get('user mail id')

    file_and_detail = web_scraping.scrapfyt(url)
    sentiment = comment_sentiment_analysis.sepposnegcom("Full Comments.csv")
    send_mail.mailsend(emailto)

    list_file_and_detail = list(file_and_detail)
    list_sentiment = list(sentiment)
    print(list_file_and_detail)
    video_title, video_owner, video_comment_with_replies, video_comment_without_replies = list_file_and_detail[1:]
    pos_comments_csv, neg_comments_csv, video_posive_comments, video_negative_comments = list_sentiment
    pos_comments_csv = pd.read_csv('Positive Comments.csv')
    neg_comments_csv = pd.read_csv('Negative Comments.csv')

    delete_files.file_delete()

    after_complete_message = "Your file is ready and sent to your mail id"

    return render_template("index.html",after_complete_message = after_complete_message, title = video_title,
                           owner = video_owner, comment_w_replies = video_comment_with_replies,
                           comment_wo_replies = video_comment_without_replies,
                           positive_comment = video_posive_comments, negative_comment = video_negative_comments,
                           pos_comments_csv = [pos_comments_csv.to_html()], neg_comments_csv = [neg_comments_csv.to_html()])

if __name__ == "app":
    app.run()

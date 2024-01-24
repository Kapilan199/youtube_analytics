from flask import Flask, render_template, request
import web_scraping, comment_sentiment_analysis, send_mail, delete_files, data_visual
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/scrap', methods = ['POST'])
def scrap_comments():
    url = request.form.get('youtube url')
    emailto = request.form.get('user mail id')

# 1. scrapes url and return file with comments and other details
    file_and_detail = web_scraping.scrapfyt(url)

# 2. takes the files and analyzes it and return the list positive and negative comments and the number of each.
    sentiment = comment_sentiment_analysis.sepposnegcom("Full_Comments.csv")



# 3. converting to list and formating
    list_file_and_detail = list(file_and_detail)
    list_sentiment = list(sentiment)
    print(list_file_and_detail)
    video_title, video_owner, video_comment_with_replies, video_comment_without_replies = list_file_and_detail[1:]
    pos_comments_csv, neg_comments_csv, video_posive_comments, video_negative_comments = list_sentiment
    pos_comments_csv = pd.read_csv('Positive_Comments.csv')
    neg_comments_csv = pd.read_csv('Negative_Comments.csv')
    print("File checking contents:")
    print(pos_comments_csv)
    print(neg_comments_csv)
    print("File checking contents:")


    numeric_part = ''.join(filter(str.isdigit, video_posive_comments))
    # Convert the numeric part to an integer
    positive_number = int(numeric_part)
    numeric_part = ''.join(filter(str.isdigit, video_negative_comments))
    # Convert the numeric part to an integer
    negative_number = int(numeric_part)

    encoded_image = data_visual.plot(positive_number, negative_number)
    # Render template with the encoded image


# 4. send the csv created by the sentiment file to the given email id
    send_mail.mailsend(emailto, encoded_image)



#  5. delete the comment files because we dont need them anymore
    delete_files.file_delete()

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

@app.route('/test1')
def test():
    # Create a CSV file
    data = {'Name': ['John', 'Jane', 'Bob'], 'Age': [25, 30, 22]}
    df = pd.DataFrame(data)
    df.to_csv('test.csv', index=False)

    # Read the CSV file
    read_df = pd.read_csv('test.csv')

    # Return the content of the CSV file
    print(read_df)
    return read_df.to_html()
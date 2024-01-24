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


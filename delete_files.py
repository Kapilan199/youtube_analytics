import os


def file_delete():
    file_to_delete = ["comments.csv", "Full_Comments.csv", "Positive_Comments.csv", "Negative_Comments.csv"]

    for f in file_to_delete:
        os.remove(f)




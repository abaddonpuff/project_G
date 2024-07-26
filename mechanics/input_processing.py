from textblob import TextBlob
import statistics
from pathlib import Path

image_folder_path = Path.cwd() / "mechanics" / "common_expressions.json"


def text_sentiment_processing(text):
    blob = TextBlob(text)

    sentiments = []

    for sentence in blob.sentences:
        sentiments.append(sentence.sentiment.polarity)

    if statistics.fmean(sentiments) > 0.3:
        return "positive"

    if statistics.fmean(sentiments) >= -0.3 and statistics.fmean(sentiments) <= 0.3:
        return "neutral"

    if statistics.fmean(sentiments) < -0.3:
        return "negative"


def process_message(text):
    blob = TextBlob(text)

    # with open(str(image_folder_path), "r") as common_text_file:
    # common_text = json.load(common_text_file)

    for sentence in blob.sentences:
        for word in sentence.words:
            print(word.correct())

    return


def main():
    text = """Hello!
        Hi therwe!
        Good morning!
        Good afternoon!"""

    print(process_message(text))


if __name__ == "__main__":
    main()

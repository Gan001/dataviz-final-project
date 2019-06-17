import requests
import json
from pprint import pprint
from config import API_KEY

class UnpackError(Exception):
    pass

class NotAString(Exception):
    pass

#calls api to perform sentimental analysis on strings
class SentimentAnalysisNLTK:
    def __init__(self):
        self.value_dict = {}
        
    def sentiment_analysis(self, *texts):
        neg_list = []
        pos_list = []
        neutral_list = []
        label_list = []

        for text in texts:
            if type(text) is list:
                raise UnpackError('Failed to unpack list, use function(*list)')
            elif type(text) is not str:
                raise NotAString('Argument must be a string')
            else:
                response = requests.post("https://japerk-text-processing.p.rapidapi.com/sentiment/",
                  headers={
                    "X-RapidAPI-Host": "japerk-text-processing.p.rapidapi.com",
                    "X-RapidAPI-Key": API_KEY,
                    "Content-Type": "application/x-www-form-urlencoded"
                  },
                  data={
                    "language": "english",
                    "text": text
                  }
                ).json()
                label_list.append(response['label'])
                neg_list.append(response['probability']['neg'])
                neutral_list.append(response['probability']['neutral'])
                pos_list.append(response['probability']['pos'])
                self.value_dict = {"text": texts, "label": label_list, "neg": neg_list, "neutral": neutral_list, "pos": pos_list}
    
    def get_sentiment(self):
        return self.value_dict
    
    def clear_sentiment(self):
        self.value_dict = {}

    def display_sentiment(self):
        pprint(self.value_dict)
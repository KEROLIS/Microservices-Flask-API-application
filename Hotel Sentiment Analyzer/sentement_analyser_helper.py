import pandas as pd 
import numpy as np 
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# reading the dataset from the CSV file
hotels_data = pd.read_csv("/mnt/0587414f-77cd-413d-b421-9bd6abd5d331/Wzzuf/Hotel Sentiment Analyzer/7282_1.csv")

# taking only data with “Hotels” value in “ categories ” column
hotels_data = hotels_data[hotels_data['categories']=="Hotels"]

def total_sentiment(hotel_name:str):
    """ This function calculates the normalized total sentiment for the hotel
            Args :
                hotel_name (string) : the hotel name as produced in the file
            Return :
                hotel_postive (float): the postive normalized value of the total sentiment reviews
                hotel_negative (float): the negative normalized value of the total sentiment reviews
    """
    # getting the reviews for a specific hotel
    hotel_data =  hotels_data[hotels_data['name']==hotel_name]

    # Check if the hotel name is exsist or not
    if len(hotel_data) == 0:
        return "The hotel {} is not exsist !".format(hotel_name)

    hotel_data_reviews = hotel_data['reviews.text'].tolist()

    # intializing the total_n_values and total_p_values for accumulation 
    total_n_values = 0
    total_p_values = 0

    # calcualting the sentiment for each text in the reviews and accumulate them 
    for review in hotel_data_reviews :
        blob = TextBlob(review, analyzer=NaiveBayesAnalyzer())
        total_n_values += blob.sentiment.p_neg
        total_p_values += blob.sentiment.p_pos

    # normalizing the values 
    hotel_postive = total_p_values / len(hotel_data_reviews)
    hotel_negative = total_n_values / len(hotel_data_reviews)

    return {"postive_sentement" :hotel_postive,"hotel_negative":hotel_negative}
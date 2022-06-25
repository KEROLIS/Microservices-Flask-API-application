from elasticsearch_dsl import connections
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from tqdm import tqdm
# reading the dataset from the CSV file
hotels_data = pd.read_csv(
    "/mnt/0587414f-77cd-413d-b421-9bd6abd5d331/Wzzuf/Hotel Sentiment Analyzer/7282_1.csv")

# establishing the connection with the elastic search API
es_client = connections.create_connection(hosts=["http://localhost:9200/"])

# taking only data with “Hotels” value in “ categories ” column
hotels_data = hotels_data[hotels_data['categories'] == "Hotels"]

# calculating the postive sentment and negative sentment for each review in the data
hotels_reviews = hotels_data['reviews.text'].tolist()
postive_value = []
negative_value = []

print("the sentment analyser process started:")
for review in tqdm(hotels_reviews):
        blob = TextBlob(review, analyzer=NaiveBayesAnalyzer())
        negative_value.append(blob.sentiment.p_neg)
        postive_value.append(blob.sentiment.p_pos)

# storing all the results of the sentment analsys in the hotels dataframe 
hotels_data['postive_sentment']=postive_value
hotels_data['negative_sentment']=negative_value

# getting the hotels names to be indexed 
hotels_names = hotels_data['name'].unique().tolist()

def hotels_indexer():
    # indexing the data of each hotel in one document
    for hotel in hotels_names:
        hotel_data = hotels_data[hotels_data['name'] == hotel]
        document = {}

        # treating the nan values that causes errors while (elastic search) parsing process  
        for col in hotel_data.columns:
            # getting the unique value of each column
            col_data = hotel_data[col].unique().tolist()

            # if it's an array and not a single unique value, we will store only the actual values (not nan values) 
            if len(col_data) > 1:
                col_data = hotel_data[col].tolist()

                # cleaning the list from nan values 
                clean_list = []
                for item in col_data:
                    if str(item) != 'nan':
                        clean_list.append(item)

                
                document[col] = clean_list

            # if it's a single unique value and not nan
            elif str(col_data[0]) != 'nan':
                document[col] = col_data[0]

        # Indexing the hotel 
        try :
            es_client.index(index="hotels", document=document)
        except Exception as e:
            return "there was an error in indexing the hotel {} !\n the error : {}".format(hotel,e)

    return "Indexing Done."
    
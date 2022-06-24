import flask
from flask import request
from sentement_analyser_helper import total_sentiment

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST'])
def home():

# if key doesn't exist, returns None
    hotel_name = request.args.get('hotel_name')
    respone=total_sentiment(hotel_name)
    return respone
app.run()
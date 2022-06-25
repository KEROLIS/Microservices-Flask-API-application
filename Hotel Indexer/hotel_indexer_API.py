from hotel_indexer_helper import hotels_indexer
import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['POST'])

def home():
    return hotels_indexer()
app.run()
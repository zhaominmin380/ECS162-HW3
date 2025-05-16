from flask import Flask, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

#load env file
load_dotenv()

#get api key from env file
NYT_API_KEY = os.getenv('NYT_API_KEY')
static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

# Mongo connection
mongo_uri = os.getenv("MONGO_URI")
mongo = MongoClient(mongo_uri)
db = mongo.get_default_database()

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
CORS(app)

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/api/news')
def get_news():
    #fetch news from davis or sac
    query = "Davis OR Sacramento"
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={NYT_API_KEY}"
    nyt_response = requests.get(url)

    if nyt_response.status_code != 200:
        return jsonify({'error': 'Failed to fetch news'}), 500

    articles = nyt_response.json().get('response', {}).get('docs', [])

    news_list = []
    for article in articles:
        multimedia = article.get('multimedia', [])
        #print("Multimedia:", multimedia)
        image_url = ''

        if isinstance(multimedia, dict):
            image_url = multimedia.get('default', {}).get('url', '')
        news_list.append({
            'headline': article.get('headline', {}).get('main', ''),
            'snippet': article.get('snippet', ''),
            'abstract': article.get('abstract', ''),
            'url': article.get('web_url', ''),
            'image': image_url
        })
    
    return jsonify(news_list)
    


@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    return send_from_directory(template_path, 'index.html')

@app.route("/test-mongo")
def test_mongo():
    return jsonify({"collections": db.list_collection_names()})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)
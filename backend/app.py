from flask import Flask, redirect, url_for, session, jsonify, send_from_directory, request
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

#load env file
load_dotenv()

#get api key from env file
NYT_API_KEY = os.getenv('NYT_API_KEY')
static_path = os.getenv('STATIC_PATH','static')
template_path = os.getenv('TEMPLATE_PATH','templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.urandom(24)

# Mongo connection
mongo_uri = os.getenv("MONGO_URI")
mongo = MongoClient(mongo_uri)
db = mongo.get_default_database()
comments_col = db['comments']
CORS(app, supports_credentials=True)

oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('http://localhost:5173')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('http://localhost:5173')

# check if user login
@app.route('/api/user')
def get_user():
    if 'user' in session:
        return jsonify({'user': session['user']})
    return jsonify({'user': None})

# get comments from user input
@app.route('/api/comments', methods=['POST'])
def post_comment():
    # only login user can comment
    if 'user' not in session:
        return jsonify({'error': 'Please login first'}), 403
    
    data = request.json
    user = session.get('user', {})

    comment = {
        "user_id": user.get('sub'),
        "username": user.get('name'),
        "article_url": data.get("article_url"),
        "content": data.get("content"),
        "parent_id": data.get("parent_id"),
        "removed": False
    }
    #print("[USER INFO]", user, flush=True)
    result = comments_col.insert_one(comment)
    # ObjectId -> string
    comment['_id'] = str(result.inserted_id)
    return jsonify(comment), 201

# get comments already in articles
@app.route('/api/comments', methods=['GET'])
def get_comments():
    article_url = request.args.get('article_url')
    if not article_url:
        return jsonify({'error': 'Missing article_url parameter'}), 400

    cursor = comments_col.find({
        "article_url": article_url,
    })

    comments = []
    for c in cursor:
        c['_id'] = str(c['_id'])
        c['parent_id'] = str(c['parent_id']) if c.get('parent_id') else None
        comments.append(c)
        # still show but delete message
        if c.get('removed') == True:
            c['content'] = 'COMMENT REMOVED BY MODERATOR!'
            c['username'] = '[deleted]'

    return jsonify(comments)

# delete specific comments
@app.route('/api/comments/<id>', methods=['DELETE'])
def delete_comment(id):
    user = session.get('user')
    # only moderator can delete
    if not user or not user.get('email', '').startswith('moderator'):
        return jsonify({'error': 'Unauthorized'}), 403
    try:
        object_id = ObjectId(id)
    except:
        return jsonify({'error': 'Invalid ID'}), 400
    
    # set 'removed' in comment to true
    result = comments_col.update_one({"_id": object_id}, {"$set": {"removed": True}})

    if result.matched_count == 0:
        return jsonify({'error': 'Comment not found'}), 404
    return jsonify({'success': True})

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

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)

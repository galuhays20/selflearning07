from flask import Flask, render_template, jsonify, request
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
connection_string='mongodb+srv://test:test123@cluster0.tlly1pu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(connection_string)
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}))
    for article in articles:
        article['_id'] = str(article['_id'])
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    mytime_post = today.strftime('%Y.%m.%d')

    files = request.files.getlist("file_give")  # Mendapatkan semua file yang diunggah

    for file in files:
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)

    profiles = request.files.getlist("profile_give")  # Mendapatkan semua file profil yang diunggah

    for profile in profiles:
        extension = profile.filename.split('.')[-1]
        profilename = f'static/profile-{mytime}.{extension}'
        profile.save(profilename)

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive.strip(),
        'content': content_receive.strip(),
        'mytime_post': mytime_post,
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'Upload complete!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000,debug=True)
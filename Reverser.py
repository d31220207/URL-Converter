from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        result = reverse_url(url)
    return render_template_string(html_template, result=result)

def reverse_url(url):
    parsed_url = urlparse(url)
    
    if 'github.io' in url:
        parts = url.split('/')
        username = parts[2].split('.')[0]
        repo_name = '/'.join(parts[3:])
        return f"https://github.com/{username}/{repo_name}"
    
    elif 'drive.google.com' in url or 'drive.usercontent.google.com' in url:
        query_params = parse_qs(parsed_url.query)
        if 'id' in query_params:
            file_id = query_params['id'][0]
            return f"https://drive.google.com/file/d/{file_id}/view"
        elif parsed_url.path.startswith('/file/d/'):
            file_id = parsed_url.path.split('/')[3]
            return f"https://drive.google.com/file/d/{file_id}/view"
    
    elif 'youtube.com' in url or 'youtu.be' in url:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            link = soup.find('link', rel='canonical')
            if link and 'channel/' in link['href']:
                channel_id = link['href'].split('channel/')[1]
                return f"https://www.youtube.com/channel/{channel_id}"
    
    return "Invalid URL. Please enter a valid GitHub Pages, YouTube Handle & Google Drive URL"

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Reverser</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Exo:ital,wght@0,100..900;1,100..900&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=PT+Mono&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Open Sans', sans-serif;
        }
        body, html {
            height: 100%;
            background: #4e54c8;
            background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);
            overflow-x: hidden;
        }
        .container {
            width: 90%;
            max-width: 900px;
            text-align: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
        }
        input[type="text"], #result {
            width: 100%;
            padding: 15px 20px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
            font-size: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        #result {
            margin-top: 20px;
            word-break: break-all;
            text-align: left;
        }
        h1 {
            font-family: 'Exo', sans-serif;
            color: white;
            margin-bottom: 10px;
            font-weight: 300;
            font-size: 2.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .subtitle {
            font-family: 'Exo', sans-serif;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 20px;
            font-size: 1rem;
            font-weight: 300;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        button {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        #convertButton {
            background: #4a90e2;
        }
        #convertButton:hover {
            background: #357ab8;
        }
        .area {
            background: #4e54c8;
            background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);
            width: 100%;
            height: 100vh;
            position: absolute;
            top: 0;
            left: 0;
        }
        .circles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        .circles li {
            position: absolute;
            display: block;
            list-style: none;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            animation: animate 25s linear infinite;
            bottom: -150px;
        }
        .circles li:nth-child(1) {
            left: 25%;
            width: 80px;
            height: 80px;
            animation-delay: 0s;
        }
        .circles li:nth-child(2) {
            left: 10%;
            width: 20px;
            height: 20px;
            animation-delay: 2s;
            animation-duration: 12s;
        }
        .circles li:nth-child(3) {
            left: 70%;
            width: 20px;
            height: 20px;
            animation-delay: 4s;
        }
        .circles li:nth-child(4) {
            left: 40%;
            width: 60px;
            height: 60px;
            animation-delay: 0s;
            animation-duration: 18s;
        }
        .circles li:nth-child(5) {
            left: 65%;
            width: 20px;
            height: 20px;
            animation-delay: 0s;
        }
        .circles li:nth-child(6) {
            left: 75%;
            width: 110px;
            height: 110px;
            animation-delay: 3s;
        }
        .circles li:nth-child(7) {
            left: 35%;
            width: 150px;
            height: 150px;
            animation-delay: 7s;
        }
        .circles li:nth-child(8) {
            left: 50%;
            width: 25px;
            height: 25px;
            animation-delay: 15s;
            animation-duration: 45s;
        }
        .circles li:nth-child(9) {
            left: 20%;
            width: 15px;
            height: 15px;
            animation-delay: 2s;
            animation-duration: 35s;
        }
        .circles li:nth-child(10) {
            left: 85%;
            width: 150px;
            height: 150px;
            animation-delay: 0s;
            animation-duration: 11s;
        }
        @keyframes animate {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
                border-radius: 0;
            }
            100% {
                transform: translateY(-1000px) rotate(720deg);
                opacity: 0;
                border-radius: 50%;
            }
        }
        .footer {
            position: absolute;
            bottom: 10px;
            left: 0;
            right: 0;
            font-family: "PT Mono", monospace;
            font-weight: 400;
            font-style: normal;
            text-align: center;
            color: rgba(255, 255, 255, 0.255);
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="area">
        <ul class="circles">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
        </ul>
    </div>
    <div class="container">
        <h1>URL Reverser</h1>
        <div class="subtitle">Support GitHub Pages, YouTube Handle & Google Drive URL</div>
        <form method="post">
            <input type="text" name="url" placeholder="Enter URL" required>
            <button type="submit" id="convertButton">Reverse</button>
        </form>
        {% if result %}
        <div id="result">
            <strong>Reversed URL:</strong> <a href="{{ result }}" target="_blank">{{ result }}</a>
        </div>
        {% endif %}
    </div>
    <div class="footer">
        Developed by Afkar (2024)
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)

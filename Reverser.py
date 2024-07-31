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
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
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
            background: #1f8b4c;
        }
        #convertButton:hover {
            background: #176839;
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
        .icons {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        .icons svg {
            position: absolute;
            display: block;
            width: 50px;
            height: 50px;
            animation: animate 25s linear infinite;
            bottom: -150px;
            fill: rgba(255, 255, 255, 0.2);
        }
        .icons svg:nth-child(1) {
            left: 25%;
            width: 80px;
            height: 80px;
            animation-delay: 0s;
        }
        .icons svg:nth-child(2) {
            left: 10%;
            width: 60px;
            height: 60px;
            animation-delay: 2s;
            animation-duration: 12s;
        }
        .icons svg:nth-child(3) {
            left: 70%;
            width: 70px;
            height: 70px;
            animation-delay: 4s;
        }
        .icons svg:nth-child(4) {
            left: 40%;
            width: 60px;
            height: 60px;
            animation-delay: 0s;
            animation-duration: 18s;
        }
        .icons svg:nth-child(5) {
            left: 65%;
            width: 50px;
            height: 50px;
            animation-delay: 0s;
        }
        .icons svg:nth-child(6) {
            left: 75%;
            width: 110px;
            height: 110px;
            animation-delay: 3s;
        }
        .icons svg:nth-child(7) {
            left: 35%;
            width: 150px;
            height: 150px;
            animation-delay: 7s;
        }
        .icons svg:nth-child(8) {
            left: 50%;
            width: 55px;
            height: 55px;
            animation-delay: 15s;
            animation-duration: 45s;
        }
        .icons svg:nth-child(9) {
            left: 20%;
            width: 45px;
            height: 45px;
            animation-delay: 2s;
            animation-duration: 35s;
        }
        .icons svg:nth-child(10) {
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
            }
            100% {
                transform: translateY(-1000px) rotate(720deg);
                opacity: 0;
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
        .copy-icon {
            cursor: pointer;
            vertical-align: middle;
            margin-right: 15px;
            font-size: 26px;
            padding: 5px;
        }
        
        #result {
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.9);
            padding: 15px 20px;
            border-radius: 10px;
            margin-top: 20px;
            word-break: break-all;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        #result a {
            flex-grow: 1;
            text-decoration: none;
            color: #4a90e2;
            padding-left: 10px;
        }
    </style>
</head>
<body>
    <div class="area">
        <div class="icons">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 210"><path d="M0,105C0,47.103,47.103,0,105,0c23.383,0,45.515,7.523,64.004,21.756l-24.4,31.696C133.172,44.652,119.477,40,105,40 c-35.841,0-65,29.159-65,65s29.159,65,65,65c28.867,0,53.398-18.913,61.852-45H105V85h105v20c0,57.897-47.103,105-105,105 S0,162.897,0,105z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 210"><path d="M0,105C0,47.103,47.103,0,105,0c23.383,0,45.515,7.523,64.004,21.756l-24.4,31.696C133.172,44.652,119.477,40,105,40 c-35.841,0-65,29.159-65,65s29.159,65,65,65c28.867,0,53.398-18.913,61.852-45H105V85h105v20c0,57.897-47.103,105-105,105 S0,162.897,0,105z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 210"><path d="M0,105C0,47.103,47.103,0,105,0c23.383,0,45.515,7.523,64.004,21.756l-24.4,31.696C133.172,44.652,119.477,40,105,40 c-35.841,0-65,29.159-65,65s29.159,65,65,65c28.867,0,53.398-18.913,61.852-45H105V85h105v20c0,57.897-47.103,105-105,105 S0,162.897,0,105z"/></svg>
        </div>
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
            <span class="material-symbols-outlined copy-icon" onclick="copyToClipboard()">content_copy</span>
            <a href="{{ result }}" target="_blank" id="reversed-url">{{ result }}</a>
        </div>
        {% endif %}
    </div>
    <div class="footer">
        Developed by Afkar (2024)
    </div>
    <script>
        function copyToClipboard() {
            var url = document.getElementById('reversed-url').textContent;
            navigator.clipboard.writeText(url).then(function() {
                alert('URL copied to clipboard!');
            }, function(err) {
                console.error('Could not copy text: ', err);
            });
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)

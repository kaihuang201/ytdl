from flask import Flask, render_template_string, request, send_file, session
from datetime import datetime
import os
import threading
from ytdl import DownloadURLs

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session persistence

download_threads = []  # Keep track of active download threads

def get_files():
    directory = "./yt_download"
    files = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                creation_time = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                files.append((filename, f"{size_mb:.2f} MB", creation_time))
    return files

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Downloader</title>
</head>
<body>
    <h3>Enter Text to Download</h3>
    <form action="/download" method="post">
        <textarea name="videourls" rows="10" cols="120"></textarea><br>
        <input type="checkbox" name="audio_only" value="true" {% if session.get('audio_only') %}checked{% endif %}> Audio Only<br>
        <button type="submit">Download</button>
    </form>
    
    <h3>Downloaded Files</h3>
    <table border="1">
        <tr>
            <th>Filename</th>
            <th>Size (MB)</th>
            <th>Creation Date & Time</th>
        </tr>
        {% for file in files %}
        <tr>
			<td><a href="{{ url_for('static', filename='yt_download/' + file[0]) }}">{{ file[0] }}</a></td>
            <td>{{ file[1] }}</td>
            <td>{{ file[2] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    files = get_files()
    return render_template_string(HTML_PAGE, files=files)

@app.route('/download', methods=['POST'])
def download():
    video_urls = [line.strip() for line in request.form.get("videourls", "").split('\n')]
    audio_only = request.form.get("audio_only") == "true"
    session['audio_only'] = audio_only  # Store choice in session
    
    '''
    thread = threading.Thread(target=DownloadURLs, args=(video_urls, audio_only))
    thread.start()
    download_threads.append(thread)
    '''
    DownloadURLs(video_urls, audio_only)
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)


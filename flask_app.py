from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__, template_folder='templates')


def get_audio_url(video):
    audio_streams = video.streams.filter(only_audio=True)
    audio_stream = audio_streams[-1]
    return audio_stream.url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download',methods=['POST'])
def download():
    yt = YouTube(request.form['url'])
    video_streams = yt.streams
    audio_stream = get_audio_url(yt)
    video_streams = sorted(video_streams, key=lambda x: int(x.resolution.split('p')[0]) if x.resolution else 0)
    for stream in video_streams:
        stream.audio_url = audio_stream
    return render_template('download.html', stream_info=video_streams)

if __name__ == '__main__':
    app.run(port=8080,debug=True)
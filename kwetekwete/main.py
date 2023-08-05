from flask import Flask, render_template, request
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""  # Initialize the message variable
    if request.method == 'POST':
        link = request.form['video_link']
        if link:
            try:
                # Download the video directly without specifying the output path
                video = YouTube(link).streams.first()
                filename = video.default_filename
                downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
                download_path = os.path.join(downloads_folder, filename)

                # Create the Downloads folder if it doesn't exist
                if not os.path.exists(downloads_folder):
                    os.makedirs(downloads_folder)

                # Download the video to the Downloads folder
                video.download(output_path=downloads_folder)

                # Check if the downloaded video file exists
                if not os.path.exists(download_path):
                    message = "Failed to save the video in the Downloads folder."
                else:
                    message = ""
            except Exception as e:
                message = f"An error occurred: {e}"
        else:
            message = "Please enter a valid YouTube URL."

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

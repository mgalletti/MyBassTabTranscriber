import os
import sys
import datetime
from loguru import logger

from flask import Flask
from flask import render_template
from flask import request
from my_bass_tab_transcriber.services.audio_service import AudioFileService


app = Flask(__name__)


def set_up_logging():
    # log file handler with rotation
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 week",
        level="INFO",
        colorize=True,
    )
    # add console handler for real-time logging
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message} | <yellow>{extra}</yellow>",
        colorize=True,
    )


set_up_logging()


# As of the moment, everythin works using a local folder. This is fine for the moment as the app runs locally
# If this will become a web app, then files needs to be loaded from a cloud storage such as AWS S3 or something.
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

UPLOAD_WEB_PAGE = "upload.html"


@app.route("/")
def home():
    return render_template(UPLOAD_WEB_PAGE)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        logger.info(f"File: {file.filename}")
        try:
            audio_file_service: AudioFileService = AudioFileService(file_path)
            audio_file_service.check_audio_loudness()
            instant_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            improved_audio_file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                f"improved_audio_file_path_{instant_str}.wav",
            )
            audio_file_service.save_as_wav(improved_audio_file_path)
        except Exception as e:
            logger.exception(f"Error processing file: {e}")
            return render_template(UPLOAD_WEB_PAGE, error=str(e))

        return render_template(
            UPLOAD_WEB_PAGE, message=f"File '{file.filename}' uploaded successfully!"
        )

    return render_template(
        UPLOAD_WEB_PAGE,
        error="Invalid file type. Please upload an MP3, WAV, or FLAC file.",
    )


if __name__ == "__main__":
    logger.info("Starting app...")
    app.run(debug=True)

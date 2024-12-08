from typing import List, Final, Optional

from my_bass_tab_transcriber.validators import BaseValidator

DEFAULT_ALLOWED_IMAGE_FILE_EXTENSION: Final[List[str]] = ["png", "jpg", "jpeg"]
DEFAULT_ALLOWED_AUDIO_FILE_EXTENSION: Final[List[str]] = ["wav", "mp3", "flac"]
DEFAULT_ALLOWED_FILE_EXTENSION: Final[List[str]] = (
    DEFAULT_ALLOWED_IMAGE_FILE_EXTENSION + DEFAULT_ALLOWED_AUDIO_FILE_EXTENSION
)


class FileValidator(BaseValidator):
    def __init__(self, allowed_file_extension: Optional[List[str]] = None):
        super().__init__()
        self.allowed_file_extension = (
            allowed_file_extension
            if allowed_file_extension
            else DEFAULT_ALLOWED_FILE_EXTENSION
        )

    def validate(self, filename: str):
        if (
            "." not in filename
            and filename.rsplit(".", 1)[1].lower() in self.allowed_file_extension
        ):
            raise ValueError(
                f"Invalid file extension. Allowed extensions: {self.allowed_file_extension}"
            )

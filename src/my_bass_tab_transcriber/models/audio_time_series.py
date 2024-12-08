import numpy as np
import librosa

from dataclasses import dataclass
from io import BytesIO, BufferedReader


@dataclass(frozen=True)
class AudioTimeSeries:
    audio: np.ndarray
    sample_rate: int

    @staticmethod
    def load_from_file(file_path: str):
        audio, sample_rate = librosa.load(file_path)
        return AudioTimeSeries(audio, sample_rate)

    @staticmethod
    def load_from_stream(stream: BytesIO):
        audio, sample_rate = librosa.load(
            BufferedReader(stream), sr=None
        )  # load keeping original sample rate
        return AudioTimeSeries(audio, sample_rate)

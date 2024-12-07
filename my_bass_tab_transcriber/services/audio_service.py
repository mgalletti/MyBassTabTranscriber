from loguru import logger
from typing import Optional
from enum import Enum
import librosa
import numpy as np
from pydub import AudioSegment
from validators.validator_factory import ValidatorFactory, ValidatorTypes
from services.file_converters import WavAudioFileConverter
from utils.audio_enhancements import AudioFileQualityImprover
from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True)
class AudioTimeSeries:
    audio: np.ndarray
    sample_rate: int
    
    @staticmethod
    def load(file_path: str):
        audio, sample_rate = librosa.load(file_path)
        return AudioTimeSeries(audio, sample_rate)


class AudioFileService:
    def __init__(self, audio_file_path: str):
        validator = ValidatorFactory(ValidatorTypes.FILE_VALIDATOR).get_instance()
        logger.info(f"Validating file '{audio_file_path}'")
        validator.validate(audio_file_path)
        self.audio_file_path = audio_file_path
        self.wav_converter = WavAudioFileConverter(validator)
        
    def save_as_wav(self, output_file: str, sample_rate: int=16000):
        logger.info(f"Converting file '{self.audio_file_path}' and saving it to '{output_file}.")
        self.wav_converter.convert_to_wav(self.audio_file_path, output_file, sample_rate)
        
    def check_audio_loudness(self, lower_threshold: float = 0.05, upper_threshold: float = 0.5):
        logger.info(f"Checking loudness of file '{self.audio_file_path}'.", extra={"lower_threshold": lower_threshold, "upper_threshold": upper_threshold})
        
        audio, _ = librosa.load(self.audio_file_path)
        rms = librosa.feature.rms(y=audio)
        avg_rms = rms.mean()
        
        logger.info(f"Average RMS: {avg_rms}")
        if avg_rms < lower_threshold:
            logger.exception(f"Audio file is too silent. Please provide a louder audio file")
            raise ValueError(f"Audio file is too silent. Please provide a louder audio file. Current RMS: {avg_rms}")
        elif avg_rms > upper_threshold:
            logger.exception(f"Audio file is too loud. Please provide a quieter audio file.")
            raise ValueError(f"Audio file is too loud. Please provide a quieter audio file. Current RMS: {avg_rms}")
        
        logger.info("Audio file loudness within range")
        
    def enhance_quality(self, output_file_copy: Optional[str] = None) -> AudioSegment:
        audio_improver = AudioFileQualityImprover(self.audio_file_path)
        audio_segment = audio_improver.enhance_quality(output_file_copy)
        return audio_segment
        
        
class AudioNormalization(Enum):
    PEAK = 1
    RMS = 2
        
    
class AudioSamplingService:
    @staticmethod
    def sample(audio_time_series: AudioTimeSeries, target_sample_rate: int = 44100) -> AudioTimeSeries:
        resampled_audio = librosa.resample(audio_time_series.audio, orig_sr=audio_time_series.sample_rate, target_sr=target_sample_rate)
        return AudioTimeSeries(resampled_audio, target_sample_rate)
        
    @staticmethod
    def normalize(audio_time_series: AudioTimeSeries, normalization_strategy: AudioNormalization = AudioNormalization.PEAK) -> AudioTimeSeries:

        pass
    

class AudioNormalizationStrategy(ABC):
    @staticmethod
    def normalize(audio: AudioTimeSeries) -> AudioTimeSeries:
        raise NotImplementedError("Normalization strategy not implemented")
    

class AudioPeakNormalizationStrategy(AudioNormalizationStrategy):
    
    @staticmethod
    def normalize(audio: AudioTimeSeries) -> AudioTimeSeries:
        audio_normalized = audio.audio / np.max(np.abs(audio.audio))
        return AudioTimeSeries(audio_normalized, audio.sample_rate)
    
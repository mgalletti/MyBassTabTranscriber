import os
from typing import Optional
from pydub import AudioSegment
from pydub.effects import normalize, low_pass_filter, high_pass_filter
import noisereduce as nr
import numpy as np
from scipy.io.wavfile import read, write
from validators.file_validators import FileValidator as AudioFileValidator, DEFAULT_ALLOWED_AUDIO_FILE_EXTENSION
from loguru import logger


class AudioSegmentQualityImprover:
    def __init__(self, audio_segment: AudioSegment, audio_file_validator: AudioFileValidator, temp_directory: str = ""):
        logger.info("Initializing audio quality improver")
        self.audio_file_validator = audio_file_validator
        self.original_audio_segment = audio_segment
        self.temp_directory = temp_directory
        # Convert to mono and standardize frame rate
        self.mono_audio_segment = audio_segment.set_channels(1).set_frame_rate(44100)
    
    # TODO: review this logic. at the moment the audio is completely distorted.. 
    def enhance_quality(self, output_audio_file: Optional[str] = None) -> AudioSegment:
        logger.info("Starting enhancing audio quality process..")
        # Check if output_audio_file is correctly formatted as a file
        if output_audio_file:
            self.audio_file_validator.validate(output_audio_file)
        # Convert to wav
        TEMP_FILE_NAME = "temp.wav"
        file_path = os.path.join(self.temp_directory, TEMP_FILE_NAME)
        self.mono_audio_segment.export(file_path, format="wav")
        logger.debug(f"Exported temporary audio segment to temp file: {file_path}")
        # Apply noise reduction
        logger.debug("Applying noise reduction..")
        rate, data = read(file_path)
        reduced_noise = nr.reduce_noise(y=data.astype(np.float32), sr=rate)
        # remove temp file
        os.remove(file_path)
        logger.debug(f"Removed temp file {file_path}.")
        # Re-create AudioSegment from processed data
        processed_audio = AudioSegment(
            reduced_noise.tobytes(),
            frame_rate=rate,
            sample_width=2,
            channels=1,
        )
        # Apply filters and normalization
        # 1. Normalize gain
        logger.debug("Normalizing gain..")
        processed_audio = normalize(processed_audio)
        # 2. Remove sub-bass
        logger.debug("Removing sub-bass..")
        processed_audio = high_pass_filter(processed_audio, cutoff=80)
        # 3. Remove high hiss
        logger.debug("Removing high hiss..")
        processed_audio = low_pass_filter(processed_audio, cutoff=8000)
        
        # Export enhanced audio
        if output_audio_file:
            logger.debug(f"Exporting enhanced audio to {output_audio_file}")
            processed_audio.export(output_audio_file, format="wav")
            
        logger.info("Finished enhancing audio quality process.")
        return processed_audio


class AudioFileQualityImprover(AudioSegmentQualityImprover):
    def __init__(self,  audio_file_path, audio_file_validator: AudioFileValidator = AudioFileValidator(allowed_file_extension=DEFAULT_ALLOWED_AUDIO_FILE_EXTENSION)):
        audio_file_validator.validate(audio_file_path)
        audio_segment = AudioSegment.from_file(audio_file_path)
        super().__init__(audio_segment, audio_file_validator)
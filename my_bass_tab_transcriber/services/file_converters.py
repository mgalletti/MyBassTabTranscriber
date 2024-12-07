import os
from pydub import AudioSegment
from validators import BaseValidator

   
class WavAudioFileConverter:
    def __init__(self, base_validator: BaseValidator):
        self.validator = base_validator
        pass
    
    def convert_to_wav(self, input_file: str, output_file: str, sample_rate: int=16000):
        """Converts input audio to:
            - `.wav` format.
            - Mono channel.
            - Fixed sample rate (e.g., 16 kHz).

        Args:
            input_file (str): input audio file path
            output_file (str): output audio file path
            sample_rate (int, optional): Sample rate. Defaults to 16000.
        """
        self.validator.validate(input_file)
        audio: AudioSegment = AudioSegment.from_file(input_file)
        audio = audio.set_frame_rate(sample_rate).set_channels(1)        
        audio.export(output_file, format="wav")

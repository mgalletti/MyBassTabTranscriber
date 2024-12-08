from enum import Enum

from my_bass_tab_transcriber.validators.file_validators import FileValidator


class ValidatorTypes(Enum):
    FILE_VALIDATOR = "file_validator"


class ValidatorFactory:
    def __init__(self, validator_type: ValidatorTypes):
        self.validator_type = validator_type

    def get_instance(self):
        if self.validator_type == ValidatorTypes.FILE_VALIDATOR:
            return FileValidator()

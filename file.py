from aeneas.audiofile import AudioFile
from aeneas.textfile import TextFile


def parse_audio_file(file_path):
    file = AudioFile(file_path=file_path)
    file.read_properties()
    return file


def parse_text_file(file_path, file_format="plain"):
    file = TextFile(file_path, file_format)
    return file

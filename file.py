from aeneas.audiofile import AudioFile as AeneasAudio
from moviepy import AudioFileClip as MoviePyAudio
from aeneas.textfile import TextFile


class AudioFile(AeneasAudio, MoviePyAudio):
    def __init__(self, file_path=None):
        AeneasAudio.__init__(self, file_path=file_path)
        MoviePyAudio.__init__(self, filename=file_path)

    def __enter__(self):
        self.read_properties()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear_data()
        self.close()


def parse_text_file(file_path, file_format="plain"):
    file = TextFile(file_path, file_format)
    return file

from file import AudioFile, parse_text_file
from audio import generate_sync_map
from video import create_video


if __name__ == "__main__":
    audio_file = input("Enter audio file path: ")
    text_file = input("Enter text file path: ")

    text = parse_text_file(text_file)
    with AudioFile(audio_file) as audio:
        sync_map = generate_sync_map(audio, text)
        create_video(audio, sync_map)

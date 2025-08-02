from file import AudioFile, parse_text_file
from audio import generate_sync_map
from video import TypingEffect, TextVideo


if __name__ == "__main__":
    audio_file = input("Enter audio file path: ")
    text_file = input("Enter text file path: ")

    text = parse_text_file(text_file)
    with AudioFile(audio_file) as audio:
        sync_map = generate_sync_map(audio, text)
        video = TextVideo(audio, sync_map, fps=24, resolution=(540, 960))
        video.effect = TypingEffect

        export_path = input("Enter export path: ")
        video.export(export_path)

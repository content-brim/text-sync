from file import parse_audio_file, parse_text_file


if __name__ == "__main__":
    audio_file = input("Enter audio file path:")
    audio = parse_audio_file(audio_file)

    text_file = input("Enter text file path:")
    text = parse_text_file(text_file)

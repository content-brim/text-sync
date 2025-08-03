from project import Project, settings, effects


if __name__ == "__main__":
    audio_file = input("Enter audio file path: ")
    text_file = input("Enter text file path: ")
    project_name = input("Enter project name: ")

    project = Project(project_name)
    project.project_settings = settings.VERTICAL_PROJECT_SETTINGS

    project.import_audio_text(audio_file, text_file)
    project.effect = effects.TypingEffect

    project.export_settings = settings.FAST_RENDER_EXPORT_SETTINGS
    project.export()

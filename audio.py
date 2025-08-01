from aeneas.executetask import ExecuteTask
from aeneas.task import Task


config_template = "task_language={language}|is_text_type=plain|os_task_file_format=json"


def generate_sync_map(audio, text, language="eng"):
    config = config_template.format(language=language)
    task = Task(config_string=config)
    task.audio_file = audio
    task.audio_file_path_absolute = audio.file_path
    task.text_file = text
    task.text_file_path_absolute = text.file_path

    ExecuteTask(task).execute()
    return task.sync_map_leaves()

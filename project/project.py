from os.path import abspath
from copy import copy
import multiprocessing

import moviepy as mpy
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

from .settings import (
    VERTICAL_PROJECT_SETTINGS,
    PROGRAMMING_TEXT_SETTINGS,
    HIGH_QUALITY_EXPORT_SETTINGS,
)


class Project:
    _default_project_settings = copy(VERTICAL_PROJECT_SETTINGS)
    _default_text_settings = copy(PROGRAMMING_TEXT_SETTINGS)
    _default_export_settings = copy(HIGH_QUALITY_EXPORT_SETTINGS)

    def __init__(self, name):
        self.name = name
        self.project_settings = self._default_project_settings
        self.text_settings = self._default_text_settings
        self.export_settings = self._default_export_settings
        self.audio, self.text = None, None
        self.timeline = None
        # TODO: Create effect sequence
        self._effect = None

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, effect):
        self._effect = effect(project=self)

    def import_audio_text(self, audio, text, language="eng"):
        config_string = f"task_language={language}|is_text_type=plain"
        task = Task(config_string)

        task.audio_file_path_absolute = abspath(audio)
        task.text_file_path_absolute = abspath(text)

        ExecuteTask(task).execute()

        self.audio = mpy.AudioFileClip(audio)
        self.timeline = task.sync_map.fragments_tree.vchildren

    def export(self):
        assert self.timeline is not None

        duration = self.audio.duration

        mask = mpy.VideoClip(
            frame_function=lambda t: self.effect(t)[:, :, 3] / 255.0,
            duration=duration,
            is_mask=True,
        )
        video = mpy.VideoClip(
            frame_function=lambda t: self.effect(t)[:, :, :3],
            duration=duration,
        ).with_mask(mask)

        composite_video = (
            mpy.CompositeVideoClip([video], self.project_settings.resolution)
            .with_audio(self.audio)
            .with_duration(duration)
        )

        filename = f"{self.name}.{self.export_settings.extension}"
        threads = multiprocessing.cpu_count()

        composite_video.write_videofile(
            filename,
            fps=self.project_settings.fps,
            preset=self.export_settings.compression,
            codec=self.export_settings.codec,
            threads=threads,
        )

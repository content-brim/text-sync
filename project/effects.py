from bisect import bisect_right

from .texts import Text


class BaseEffect:
    def __init__(self, project):
        self.project = project

    def __call__(self, timestamp):
        timeline = self.project.timeline
        content = ""
        for i in range(1, len(timeline)):
            fragment = timeline[i]
            if fragment.begin > timestamp:
                content = self.project.timeline[i - 1].text
                break

        text = Text(self.project).with_text(content)
        return text.render()


class TypingEffect(BaseEffect):
    def __init__(self, project):
        super().__init__(project)
        self.compute_time_per_char()
        self.compute_timestamps_text()

    def compute_time_per_char(self):
        self.time_per_char = self.project.audio.duration
        for fragment in self.project.timeline:
            length = len(fragment.text)
            if length == 0:
                continue
            duration = fragment.end - fragment.begin
            time = float(duration) / float(length)
            if time < self.time_per_char:
                self.time_per_char = time

    def compute_timestamps_text(self):
        self.timestamps = []
        self.texts = []
        full_text = ""
        for fragment in self.project.timeline:
            current_time = float(fragment.begin)
            for char in fragment.text:
                full_text += char
                self.timestamps.append(current_time)
                self.texts.append(full_text)
                current_time += self.time_per_char
            full_text += "\n"

    def get_text_at(self, timestamp):
        idx = bisect_right(self.timestamps, timestamp) - 1
        if idx >= 0:
            return self.texts[idx]
        return ""

    def __call__(self, timestamp):
        content = self.get_text_at(timestamp)
        text = Text(self.project).with_text(content)
        return text.render()

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

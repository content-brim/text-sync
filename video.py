from moviepy import TextClip, CompositeVideoClip, VideoClip


class TypingEffect:
    def __init__(self, video):
        self.video = video
        self.timeline = self._build_timeline(video.sync_map)
        self.frames_cache = {}

    def _build_timeline(self, sync_map):
        timed_text = []
        full_text = ""

        for fragment in sync_map[1:-1]:
            text = fragment.text.strip()
            if not text:
                continue

            start = float(fragment.begin)
            end = float(fragment.end)
            duration = end - start
            char_delay = duration / max(len(text), 1)

            for i, char in enumerate(text):
                t = start + i * char_delay
                full_text += char
                timed_text.append((t, full_text))

            full_text += "\n"

        return timed_text

    def get_text_at(self, t):
        for i in range(len(self.timeline) - 1, -1, -1):
            if t >= self.timeline[i][0]:
                text = self.timeline[i][1]
                return text
        return ""

    def __call__(self, timestamp):
        text = self.get_text_at(timestamp).strip()
        if text in self.frames_cache:
            return self.frames_cache[text]

        size = list(self.video.resolution)
        size[0] -= 100
        size[1] -= 100

        clip = TextClip(
            text=text,
            font="Courier.ttf",
            font_size=24,
            color="#60bef6",
            bg_color=None,
            transparent=True,
            method="caption",
            horizontal_align="left",
            vertical_align="top",
            size=size,
        )
        frame = clip.get_frame(0)
        self.frames_cache[text] = frame
        return frame


class TextVideo:
    def __init__(self, audio, sync_map, fps=60, resolution=(1080, 1920)):
        self.audio = audio
        self.sync_map = sync_map
        self.fps = fps
        self.resolution = resolution
        self._effect = None

    def get_effect(self):
        return self._effect

    def set_effect(self, effect_class):
        self._effect = effect_class(self)

    effect = property(get_effect, set_effect)

    def export(self, path):
        if self.effect is None:
            raise ValueError("No effect set.")

        duration = self.audio.duration + 2
        video = VideoClip(
            frame_function=self.effect,
            duration=duration,
        ).with_position((50, 50))

        result = (
            CompositeVideoClip([video], size=self.resolution)
            .with_background_color(color=(31, 31, 31))
            .with_audio(self.audio)
            .with_duration(3)
        )

        result.write_videofile(path, fps=self.fps, threads=4, preset="ultrafast")

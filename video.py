from moviepy import CompositeVideoClip, VideoClip
import gizeh as gz


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

    def render_text(self, text):
        width, height = self.video.resolution
        surface = gz.Surface(width - 100, height - 100)
        text_box = gz.text(
            text,
            fontfamily="Courier.ttf",
            fontweight="normal",
            fontsize=24,
            fill=(0.23, 0.74, 0.96, 1),
            xy=(100, 100),
        )
        text_box.draw(surface)
        return surface.get_npimage(transparent=True)

    def __call__(self, timestamp):
        text = self.get_text_at(timestamp)
        return self.render_text(text)


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

        duration = self.audio.duration
        video_mask = VideoClip(
            frame_function=lambda t: self.effect(t)[:, :, 3] / 255.0,
            duration=duration,
            is_mask=True,
        ).with_position((50, 50))
        video = (
            VideoClip(
                frame_function=lambda t: self.effect(t)[:, :, :3],
                duration=duration,
            )
            .with_position((50, 50))
            .with_mask(video_mask)
        )

        result = (
            CompositeVideoClip([video], size=self.resolution)
            .with_background_color(color=(31, 31, 31))
            .with_audio(self.audio)
            .with_duration(3)
        )

        result.write_videofile(path, fps=self.fps, threads=4, preset="ultrafast")

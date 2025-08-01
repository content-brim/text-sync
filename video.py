from moviepy import TextClip, CompositeVideoClip


def create_video(audio, sync_map):
    clips = []
    for fragment in sync_map:
        text = fragment.text
        start = float(fragment.begin)
        end = float(fragment.end)
        duration = end - start

        text_clip = (
            TextClip(text=text, font_size=20, color="green", size=(1080, 200))
            .with_start(start)
            .with_duration(duration)
            .with_position("center", "bottom")
        )
        clips.append(text_clip)

    video = (
        CompositeVideoClip(clips, size=(1080, 1920))
        .with_audio(audio)
        .with_duration(audio.duration)
    )
    video.preview(fps=25)

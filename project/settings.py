from dataclasses import dataclass, field


@dataclass
class ProjectSettings:
    resolution: list
    fps: int


HORIZONTAL_PROJECT_SETTINGS = (
    lambda: ProjectSettings(resolution=[1920, 1080], fps=30)
)()
VERTICAL_PROJECT_SETTINGS = (lambda: ProjectSettings(resolution=[1080, 1920], fps=30))()


@dataclass
class ExportSettings:
    compression: str
    extension: str
    codec: str


HIGH_QUALITY_EXPORT_SETTINGS = (
    lambda: ExportSettings(
        compression="veryslow",
        extension="avi",
        codec="rawvideo",
    )
)()
FAST_RENDER_EXPORT_SETTINGS = (
    lambda: ExportSettings(
        compression="ultrafast",
        extension="webm",
        codec="libvpx",
    )
)()


@dataclass
class TextSettings:
    font_size: int
    font_family: str
    color: list = field(default_factory=lambda: [0, 0, 0, 100])
    alignment: list = field(default_factory=lambda: ["left", "top"])
    margin: list = field(default_factory=lambda: [0, 0, 0, 0])


PROGRAMMING_TEXT_SETTINGS = (
    lambda: TextSettings(14, "Courrier.ttf", color=[107, 152, 85, 100])
)()

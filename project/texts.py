import textwrap

import gizeh as gz


class Text:
    def __init__(self, project):
        self.project = project
        self.text = project.timeline[0].text
        self._color = None

        self.font_kwargs = {
            "fontsize": project.text_settings.font_size,
            "fontfamily": project.text_settings.font_family,
        }
        self.align_kwargs = {
            "h_align": project.text_settings.alignment[0],
            "v_align": project.text_settings.alignment[1],
        }
        self.line_spacing_multiplier = (
            self.project.text_settings.line_spacing_multiplier
        )
        self.color = project.text_settings.color
        self.font_kwargs = {
            "fontsize": project.text_settings.font_size,
            "fontfamily": project.text_settings.font_family,
        }
        self.margin = project.text_settings.margin
        self.compute_line_space()
        self.compute_size()
        self.compute_position()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = [color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 100]

    def with_color(self, red, green, blue, alpha):
        self.color = [red, green, blue, alpha]
        return self

    def with_alignment(self, horizontal, vertical):
        self.align_kwargs = {"h_align": horizontal, "v_align": vertical}
        return self

    def with_text(self, text):
        width_factor = 0.6
        max_chars_per_line = int(
            (self.size_kwargs["width"]) / (self.font_kwargs["fontsize"] * width_factor)
        )
        self.text = textwrap.wrap(text, width=max_chars_per_line)
        self.compute_line_space()
        return self

    def with_font(self, font_size, font_family):
        self.font_kwargs = {
            "fontsize": font_size,
            "fontfamily": font_family,
        }
        return self

    def with_margin(self, top, right, bottom, left):
        self.margin = [top, right, bottom, left]
        self.compute_size()
        self.compute_position()
        return self

    def with_line_spacing_multiplier(self, multiplier):
        self.line_spacing_multiplier = multiplier
        self.compute_line_space()
        return self

    def compute_line_space(self):
        self.line_space = self.font_kwargs["fontsize"] * self.line_spacing_multiplier
        self.compute_position()

    def compute_size(self):
        width = (
            self.project.project_settings.resolution[0]
            - self.margin[1]
            - self.margin[3]
        )
        height = (
            self.project.project_settings.resolution[1]
            - self.margin[0]
            - self.margin[2]
        )
        self.size_kwargs = {"width": width, "height": height}

    def compute_position(self):
        match self.align_kwargs["h_align"]:
            case "left":
                x = self.margin[3]
            case "center":
                x = self.project.project_settings.resolution[0] / 2
            case "right":
                x = self.project.project_settings.resolution[0] - self.margin[1]

        total_height = len(self.text) * self.line_space
        match self.align_kwargs["v_align"]:
            case "top":
                y = self.font_kwargs["fontsize"] + self.margin[0]
            case "center":
                y = (
                    self.project.project_settings.resolution[1] / 2
                    - total_height / 2
                    + self.line_space / 2
                )
            case "bottom":
                y = (
                    self.project.project_settings.resolution[1]
                    - self.margin[0]
                    - self.margin[2]
                    - self.font_kwargs["fontsize"]
                    - total_height
                    + self.line_space / 2
                )

        self.position = [x, y]

    def render(self):
        surface = gz.Surface(**self.size_kwargs)
        line_space = (
            self.font_kwargs["fontsize"]
            * self.project.text_settings.line_spacing_multiplier
        )
        x, y = self.position
        for line in self.text:
            text = gz.text(
                line,
                fill=self.color,
                xy=[x, y],
                **self.font_kwargs,
                **self.align_kwargs,
            )
            text.draw(surface)
            y += line_space
        return surface.get_npimage(transparent=True)

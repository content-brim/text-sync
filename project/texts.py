import gizeh as gz


class Text:
    def __init__(self, project):
        self.project = project
        self.text: str = project.timeline[0].text

        self.with_color(*project.text_settings.color)
        self.with_alignment(*project.text_settings.alignment)
        self.font_kwargs = {"fontsize": project.text_settings.font_size}
        self.with_margin(*project.text_settings.margin)
        self.with_font(
            project.text_settings.font_size,
            project.text_settings.font_family,
        )

    def with_color(self, red, green, blue, alpha):
        self.color = [red / 255, green / 255, blue / 255, alpha / 100]
        return self

    def with_alignment(self, horizontal, vertical):
        self.align_kwargs = {"h_align": horizontal, "v_align": vertical}
        return self

    def with_text(self, text):
        self.text = text
        self.compute_size()
        return self

    def with_font(self, font_size, font_family):
        self.font_kwargs = {
            "fontsize": font_size,
            "fontfamily": font_family,
        }
        self.compute_size()
        self.compute_position()
        return self

    def with_margin(self, top, right, bottom, left):
        self.margin = [top, right, bottom, left]
        self.compute_size()
        self.compute_position()
        return self

    def compute_size(self):
        lines = self.text.split("\n")
        symbols_height = len(lines)
        symbols_width = 0
        for l in lines:
            width = len(l)
            if width > symbols_width:
                symbols_width = width

        width = (
            symbols_width * self.font_kwargs["fontsize"]
            - self.margin[1]
            - self.margin[3]
        )
        height = (
            symbols_height * self.font_kwargs["fontsize"]
            - self.margin[0]
            - self.margin[2]
        )
        self.size_kwargs = {"width": width, "height": height}

    def compute_position(self):
        x = 0
        if self.align_kwargs["h_align"] == "center":
            x = self.size_kwargs["width"] / 2
        elif self.align_kwargs["h_align"] == "right":
            x = self.size_kwargs["width"]

        y = 0
        if self.align_kwargs["v_align"] == "center":
            y = self.size_kwargs["height"] / 2
        elif self.align_kwargs["v_align"] == "bottom":
            y = self.size_kwargs["height"]

        x += self.margin[3]
        y += self.font_kwargs["fontsize"] + self.margin[0]
        self.position = [x, y]

    def render(self):
        surface = gz.Surface(**self.size_kwargs)
        text = gz.text(
            self.text,
            fill=self.color,
            xy=self.position,
            **self.font_kwargs,
            **self.align_kwargs,
        )
        text.draw(surface)
        return surface.get_npimage(transparent=True)

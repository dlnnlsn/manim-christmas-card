from manim import *

edwardian_script = TexTemplate(preamble=r"""
\usepackage[no-math]{fontspec}
\setmainfont[Mapping=tex-text]{Edwardian Script ITC}
\usepackage[defaultmathsizes]{mathastext}""",
tex_compiler="xelatex",
output_format=".xdv")

class ChristmasCard(Scene):

    def construct(self):
        message = Tex("Merry Christmas", tex_template=edwardian_script)
        self.play(Write(message), run_time=3)
        self.wait()


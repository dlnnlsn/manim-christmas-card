from manim import *

edwardian_script = TexTemplate(preamble=r"""
\usepackage[no-math]{fontspec}
\setmainfont[Mapping=tex-text]{Edwardian Script ITC}
\usepackage[defaultmathsizes]{mathastext}""",
tex_compiler="xelatex",
output_format=".xdv")

GREETING = "To [Recipient]..."
SIGNOFF = "From [Sender]"

class ChristmasCard(Scene):

    def construct(self):
        if GREETING:
            greeting = Tex(GREETING, tex_template=edwardian_script)
            greeting.to_corner(UL)
            self.play(Write(greeting), run_time=3)

        message = Tex("Merry Christmas", tex_template=edwardian_script)
        self.play(Write(message), run_time=3)
        self.wait()

        if SIGNOFF:
            signoff = Tex(SIGNOFF, tex_template=edwardian_script)
            signoff.to_corner(DR)
            self.play(Write(signoff), run_time=3)
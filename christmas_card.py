from manim import *
import argparse
import os
from manim._config.main_utils import parse_args

edwardian_script = TexTemplate(preamble=r"""
\usepackage[no-math]{fontspec}
\setmainfont[Mapping=tex-text]{Edwardian Script ITC}
\usepackage[defaultmathsizes]{mathastext}""",
tex_compiler="xelatex",
output_format=".xdv")

class ChristmasCard(Scene):

    def __init__(self, to=None, sender=None, greeting="To", signoff="From", *args, **kwargs):
        super(ChristmasCard, self).__init__(*args, **kwargs)
        self.to = to
        self.sender = sender
        self.greeting = greeting
        self.signoff=signoff

    def construct(self):
        if self.to is not None:
            greeting_message = self.greeting + " " + self.to
            greeting = Tex(greeting_message, tex_template=edwardian_script)
            greeting.to_corner(UL)
            self.play(Write(greeting), run_time=3)

        message = Tex("Merry Christmas", tex_template=edwardian_script)
        self.play(Write(message), run_time=3)
        self.wait()

        if self.sender is not None:
            signoff_message = self.signoff + " " + self.sender
            signoff = Tex(signoff_message, tex_template=edwardian_script)
            signoff.to_corner(DR)
            self.play(Write(signoff), run_time=3)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--to")
    parser.add_argument("--sender")
    parser.add_argument("--greeting", default="To")
    parser.add_argument("--signoff", default="From")

    args, remaining_args = parser.parse_known_args()
    manim_args = parse_args(remaining_args + ["christmas_card.py"])
    config.digest_args(manim_args)

    scene = ChristmasCard(args.to, args.sender, args.greeting, args.signoff)
    scene.render()
    os.startfile(scene.renderer.file_writer.movie_file_path)
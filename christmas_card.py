from manimlib.imports import *

class ChristmasCard(Scene):

    def construct(self):
        message = TextMobject("Merry Christmas")
        self.play(Write(message), run_time=3)
        self.wait()


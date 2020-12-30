from manim import *
import functools
import itertools
import random

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
        tree = VGroup(Polygon(np.array([4, 2, 0]), np.array([2.25, -2, 0]), np.array([5.75, -2, 0]), color=GREEN))
        trunk = VGroup(Rectangle(height=1.5, width=1, color=ORANGE))
        trunk.next_to(tree, DOWN, buff=0)
        self.play(ShowCreation(trunk), ShowCreation(tree))
        
        for _ in range(5):
            next_iter = next_sierpinski_iteration(tree)
            self.play(Transform(tree, next_iter))

        for _ in range(30):
            triangle = random.choice(tree.submobjects)
            weights = np.random.rand(len(triangle.get_vertices()))
            weights /= sum(weights)
            bauble_pt = weights.dot(np.array(triangle.get_vertices()))
            self.play(FadeIn(Dot(point=bauble_pt, color=random_bright_color())), run_time=0.1)

        star = Tex("$\star$", color=YELLOW)
        star.scale(2)
        star.next_to(tree, UP, buff=0)
        self.add(star)

        if GREETING:
            greeting = Tex(GREETING, tex_template=edwardian_script)
            greeting.scale(2)
            greeting.to_corner(UL)
            self.play(Write(greeting), run_time=3)

        message = Tex("Merry Christmas", tex_template=edwardian_script)
        message.scale(2)
        self.play(Write(message), run_time=3)
        self.wait()

        if SIGNOFF:
            signoff = Tex(SIGNOFF, tex_template=edwardian_script)
            signoff.scale(2)
            signoff.to_corner(DR)
            self.play(Write(signoff), run_time=3)

def divide_triangle(triangle):
    assert isinstance(triangle, Polygon)
    vertices = list(triangle.get_vertices())
    midpoints = list(itertools.starmap(lambda x, y: (x + y)/2, zip(vertices, vertices[1:] + [vertices[0]])))
    return itertools.starmap(functools.partial(Polygon, color=triangle.color), zip(vertices, midpoints, [midpoints[-1]] + midpoints))

def next_sierpinski_iteration(triangles):
    return VGroup(*itertools.chain(*map(divide_triangle, triangles.submobjects)))

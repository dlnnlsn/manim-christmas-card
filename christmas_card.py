from manim import *
import itertools

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
        t1 = Polygon(np.array([4, 2, 0]), np.array([2.5, -2, 0]), np.array([5.5, -2, 0]), color=GREEN)
        tree = VGroup(t1)
        self.play(ShowCreation(tree))
        for i in range(5):
            next_iter = next_sierpinski_iteration(tree)
            self.play(Transform(tree, next_iter))

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

def divide_triangle(triangle):
    assert isinstance(triangle, Polygon)
    vertices = list(triangle.get_vertices())
    midpoints = list(map(lambda pts: (pts[0] + pts[1])/2, zip(vertices, vertices[1:] + [vertices[0]])))
    return map(lambda triple: Polygon(*triple, color=triangle.color), zip(vertices, midpoints, [midpoints[-1]] + midpoints))

def next_sierpinski_iteration(triangles):
    return VGroup(*itertools.chain(*map(divide_triangle, triangles.submobjects)))

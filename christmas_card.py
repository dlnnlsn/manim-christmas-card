from manim import *
import functools
import itertools
import random

GREETING = "To [Recipient]..."
SIGNOFF = "From [Sender]"
FONT = "Edwardian Script ITC"
FONT_SIZE = 1.5

class ChristmasCard(Scene):

    def construct(self):
        tree = VGroup(Polygon(np.array([0, 2, 0]), np.array([-1.75, -2, 0]), np.array([1.75, -2, 0]), color=GREEN))
        trunk = VGroup(Rectangle(height=1.5, width=1, color=ORANGE))
        tree.to_edge(RIGHT, buff=1)
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
            greeting = Text(GREETING, font=FONT, size=FONT_SIZE)
            greeting.to_corner(UL)
            self.play(Write(greeting), run_time=3)

        message = Text("Merry Christmas", font=FONT, size=FONT_SIZE)
        self.play(Write(message), run_time=3)
        self.wait()

        if SIGNOFF:
            signoff = Text(SIGNOFF, font=FONT, size=FONT_SIZE)
            signoff.to_corner(DR)
            self.play(Write(signoff), run_time=3)

def divide_triangle(triangle):
    assert isinstance(triangle, Polygon)
    vertices = list(triangle.get_vertices())
    midpoints = list(itertools.starmap(lambda x, y: (x + y)/2, zip(vertices, vertices[1:] + [vertices[0]])))
    return itertools.starmap(functools.partial(Polygon, color=triangle.color), zip(vertices, midpoints, [midpoints[-1]] + midpoints))

def next_sierpinski_iteration(triangles):
    return VGroup(*itertools.chain(*map(divide_triangle, triangles.submobjects)))

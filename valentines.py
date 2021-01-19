from manim import *

class SpokedMobject(VMobject):
    def __init__(self, base_mobject, num_spokes = 72, **kwargs):
        super().__init__(**kwargs)
        self.num_spokes = num_spokes
        self.base_mobject = base_mobject
        for alpha in np.linspace(0, 1 - 1/num_spokes, num_spokes):
            self.start_new_path(ORIGIN)
            self.add_line_to(base_mobject.point_from_proportion(alpha))


def BasicHeart(**kwargs):
    def heart_function(t):
        start_angle = np.arctan(-4/3)
        if t <= 1:
            return interpolate(DOWN, np.array([4/5, -2/5, 0]), t)
        elif t <= 2:
            theta = interpolate(start_angle, np.pi, t - 1)
            return 1/2 * (1 + np.cos(theta)) * RIGHT + 1/2 * np.sin(theta) * UP
        elif t <= 3:
            theta = interpolate(0, np.pi - start_angle, t - 2)
            return 1/2 * (-1 + np.cos(theta)) * RIGHT + 1/2 * np.sin(theta) * UP
        return interpolate(np.array([-4/5, -2/5, 0]), DOWN, t - 3)

    return ParametricFunction(
        heart_function,
        t_max = 4,
        **kwargs
    )

def FancyHeart(**kwargs):
    def heart_function(theta):
        x = 16 * np.sin(theta)**3
        y = 13 * np.cos(theta) - 5 * np.cos(2 * theta) - 2 * np.cos(3 * theta) - np.cos(4 * theta)
        return np.array([-x, y, 0]) / 20

    return ParametricFunction(
        heart_function,
        t_max = 2*np.pi,
        **kwargs
    )

class ValentinesScene(Scene):
    def construct(self):
        scale_factor = 3/4
        xbuf = config.frame_width / 40
        ybuf = xbuf * 3/4
        complete_pairs = int((config.frame_width - xbuf) / ((2 + 8/5) * scale_factor + 2 * xbuf))
        extra = (config.frame_width - xbuf - complete_pairs * (2 + 8/5) * scale_factor - 2 * complete_pairs * xbuf) >= (2 * scale_factor + xbuf)
        rows = int((config.frame_height - ybuf) / (ybuf + 3/2 * scale_factor))
        odd_x_padding = config.frame_width - complete_pairs * (2 + 8/5) * scale_factor - 2 * complete_pairs * xbuf + xbuf
        if extra: odd_x_padding -= (xbuf + 8/5 * scale_factor)
        odd_x_padding /= 2
        even_x_padding = config.frame_width - complete_pairs * (2 + 8/5) * scale_factor - 2 * complete_pairs * xbuf + xbuf
        if extra: even_x_padding -= (xbuf + 2 * scale_factor)
        even_x_padding /= 2
        hearts_per_row = 2 * complete_pairs
        if extra: hearts_per_row += 1
        y_padding = config.frame_height - rows * (3/2 * scale_factor + ybuf) + ybuf
        y_padding /= 2


        Basic = BasicHeart()
        Fancy = FancyHeart()
        hearts = [[None] * hearts_per_row for _ in range(rows)]
        for y in range(0, rows, 2):
            for x in range(0, hearts_per_row, 2):
                hearts[y][x] = SpokedMobject(Basic, color=RED)
                hearts[y][x].scale(scale_factor).move_to(
                    (even_x_padding + x//2 * ((2 + 8/5) * scale_factor + 2 * xbuf) + scale_factor - config.frame_x_radius) * RIGHT +
                    (y_padding + y * (3/2 * scale_factor + ybuf) + 1/2 * scale_factor - config.frame_y_radius) * DOWN
                )
                self.play(Write(hearts[y][x]))
            for x in range(1, hearts_per_row, 2):
                hearts[y][x] = SpokedMobject(Fancy, color=PINK)
                hearts[y][x].scale(scale_factor).move_to(
                    (even_x_padding + x//2 * ((2 + 8/5) * scale_factor + 2 * xbuf) + 2 * scale_factor + xbuf + 4/5 * scale_factor - config.frame_x_radius) * RIGHT +
                    (y_padding + y * (3/2 * scale_factor + ybuf) + 1/2 * scale_factor - config.frame_y_radius) * DOWN
                )
                self.play(Write(hearts[y][x]))
        for y in range(1, rows, 2):
            for x in range(0, hearts_per_row, 2):
                hearts[y][x] = SpokedMobject(Fancy, color=PINK)
                hearts[y][x].scale(scale_factor).move_to(
                    (odd_x_padding + x//2 * ((2 + 8/5) * scale_factor + 2 * xbuf) + 4/5 * scale_factor - config.frame_x_radius) * RIGHT +
                    (y_padding + y * (3/2 * scale_factor + ybuf) + 1/2 * scale_factor - config.frame_y_radius) * DOWN
                )
                self.play(Write(hearts[y][x]))
            for x in range(1, hearts_per_row, 2):
                hearts[y][x] = SpokedMobject(Basic, color=RED)
                hearts[y][x].scale(scale_factor).move_to(
                    (odd_x_padding + x//2 * ((2 + 8/5) * scale_factor + 2 * xbuf) + 4/5 * scale_factor + xbuf + 2 * scale_factor - config.frame_x_radius) * RIGHT +
                    (y_padding + y * (3/2 * scale_factor + ybuf) + 1/2 * scale_factor - config.frame_y_radius) * DOWN
                )
                self.play(Write(hearts[y][x]))

        message = Text("Happy Valentine's Day")
        self.play(Write(message))
        self.wait(5)



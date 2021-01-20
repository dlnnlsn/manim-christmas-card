from manim import *

import itertools

FONT = "Edwardian Script ITC"
FONT_SIZE = 1.5

HEARTS_PER_ROW = 10
BASIC_HEART_WIDTH = 2
FANCY_HEART_WIDTH = 8 / 5
INTER_HEART_SPACING = BASIC_HEART_WIDTH / 10

HEART_HEIGHT = 3 / 2
HEART_TOP_HEIGHT = 1 / 2
VERTICAL_INTER_HEART_SPACING = HEART_HEIGHT / 10

total_space_taken_by_hearts = (
    HEARTS_PER_ROW
    // 2
    * (BASIC_HEART_WIDTH + FANCY_HEART_WIDTH + 2 * INTER_HEART_SPACING)
    + INTER_HEART_SPACING
)
if HEARTS_PER_ROW % 2 == 1:
    total_space_taken_by_hearts += INTER_HEART_SPACING + BASIC_HEART_WIDTH

SCALE_FACTOR = config.frame_width / total_space_taken_by_hearts

BASIC_HEART_WIDTH *= SCALE_FACTOR
FANCY_HEART_WIDTH *= SCALE_FACTOR
HEART_HEIGHT *= SCALE_FACTOR
HEART_TOP_HEIGHT *= SCALE_FACTOR
INTER_HEART_SPACING *= SCALE_FACTOR
VERTICAL_INTER_HEART_SPACING *= SCALE_FACTOR

NUMBER_OF_ROWS = int(
    (config.frame_height - VERTICAL_INTER_HEART_SPACING)
    / (HEART_HEIGHT + VERTICAL_INTER_HEART_SPACING)
)
VERTICAL_PADDING = (
    config.frame_height
    - VERTICAL_INTER_HEART_SPACING
    - NUMBER_OF_ROWS * (HEART_HEIGHT + VERTICAL_INTER_HEART_SPACING)
) / 2


class SpokedMobject(VMobject):
    def __init__(self, base_mobject, num_spokes=72, **kwargs):
        super().__init__(**kwargs)
        self.num_spokes = num_spokes
        self.base_mobject = base_mobject
        for alpha in np.linspace(0, 1 - 1 / num_spokes, num_spokes):
            self.start_new_path(ORIGIN)
            self.add_line_to(base_mobject.point_from_proportion(alpha))


def BasicHeart(**kwargs):
    start_angle = np.arctan(-4 / 3)
    arc_length = 0.5 * (np.pi - start_angle)

    def heart_function(t):
        if t <= 1:
            return interpolate(DOWN, np.array([4 / 5, -2 / 5, 0]), t)
        elif t <= 1 + arc_length:
            theta = interpolate(start_angle, np.pi, (t - 1) / arc_length)
            return 1 / 2 * (1 + np.cos(theta)) * RIGHT + 1 / 2 * np.sin(theta) * UP
        elif t <= 1 + 2 * arc_length:
            theta = interpolate(
                0, np.pi - start_angle, (t - 1 - arc_length) / arc_length
            )
            return 1 / 2 * (-1 + np.cos(theta)) * RIGHT + 1 / 2 * np.sin(theta) * UP
        return interpolate(np.array([-4 / 5, -2 / 5, 0]), DOWN, t - 1 - 2 * arc_length)

    return ParametricFunction(heart_function, t_max=2 + 2 * arc_length, **kwargs)


def FancyHeart(**kwargs):
    def heart_function(theta):
        x = 16 * np.sin(theta) ** 3
        y = (
            13 * np.cos(theta)
            - 5 * np.cos(2 * theta)
            - 2 * np.cos(3 * theta)
            - np.cos(4 * theta)
        )
        return np.array([-x, y, 0]) / 20

    return ParametricFunction(heart_function, t_max=2 * np.pi, **kwargs)


class ValentinesScene(Scene):
    def construct(self):
        Basic = BasicHeart()
        Fancy = FancyHeart()
        hearts = [[None] * HEARTS_PER_ROW for _ in range(NUMBER_OF_ROWS)]

        ycoord = (
            VERTICAL_PADDING
            + VERTICAL_INTER_HEART_SPACING
            + HEART_TOP_HEIGHT
            - config.frame_y_radius
        )
        for y in range(NUMBER_OF_ROWS):
            xcoord = INTER_HEART_SPACING + BASIC_HEART_WIDTH / 2 - config.frame_x_radius
            for x in range(HEARTS_PER_ROW):
                is_basic_heart = (y + x) % 2 == 0
                color = RED if is_basic_heart else PINK
                shape = Basic if is_basic_heart else Fancy
                hearts[y][x] = (
                    SpokedMobject(shape, color=color)
                    .scale(SCALE_FACTOR)
                    .move_to(xcoord * RIGHT + ycoord * DOWN)
                )
                xcoord += (
                    BASIC_HEART_WIDTH + FANCY_HEART_WIDTH
                ) / 2 + INTER_HEART_SPACING
            ycoord += HEART_HEIGHT + VERTICAL_INTER_HEART_SPACING

        self.play(AnimationGroup(*map(Write, itertools.chain(*hearts)), lag_ratio=0.1))
        message = Text("Happy Valentine's Day!", font=FONT, size=FONT_SIZE)
        bounding_rectangle = Rectangle(
            width=message.get_width() * 1.2,
            height=message.get_height() * 1.6,
            fill_color=BLACK,
            fill_opacity=1,
        )
        self.play(FadeIn(bounding_rectangle))
        self.play(Write(message))
        self.wait()

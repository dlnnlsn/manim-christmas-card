from manim import *
import random
import math
from operator import itemgetter
from colour import Color

explosion_height = 3/4 * config.frame_height
explosion_time = 5

gravity_y = -2 * explosion_height / explosion_time**2
initial_velocity_y = -gravity_y * explosion_time

gravity = gravity_y * UP

message = "Happy New Year!"

class FireworkScene(Scene):

    def reference_colors(self, alpha):
        interval_width = 1/(2 * len(message))
        hue = alpha * (1 - 2* interval_width)
        return (Color(hsl=((hue - interval_width) % 1, 1, 0.5)), Color(hsl=((hue + interval_width) % 1, 1, 0.5)))

    def final_position(self, alpha):
        left_edge = -config.frame_x_radius + 1.5 * config.frame_width / (len(message) + 1)
        right_edge = -left_edge
        return np.array([interpolate(left_edge, right_edge, alpha), 1/2 * config.frame_y_radius, 0])

    def initial_position(self, alpha):
        return np.array([interpolate(-config.frame_x_radius/2, config.frame_x_radius/2, alpha), -config.frame_y_radius, 0])

    def arrival_time(self, alpha):
        return 5

    def flight_time(self, alpha):
        deltaH = (self.final_position(alpha) - self.initial_position(alpha))[1]
        return math.sqrt(-2 * deltaH / gravity_y)

    def start_time(self, alpha):
        return self.arrival_time(alpha) - self.flight_time(alpha)

    def initial_velocity(self, alpha):
        deltaX = (self.final_position(alpha) - self.initial_position(alpha))[0]
        time = self.flight_time(alpha)
        return np.array([deltaX / time, -gravity_y * time, 0])

    def screen_exit_time(self, alpha):
        final_height = self.final_position(alpha)[1] + config.frame_y_radius
        return math.sqrt(-2 * final_height / gravity_y) + self.arrival_time(alpha)

    def construct(self):
        alphas = np.linspace(0, 1, len(message))
        launch_sequence = sorted(enumerate(zip(map(self.start_time, alphas), alphas)), key=itemgetter(1))
        earliest_start = launch_sequence[0][1][0]
        launch_sequence = [(index, time - earliest_start, alpha) for (index, (time, alpha)) in launch_sequence]

        previous_time = 0
        for (index, time, alpha) in launch_sequence:
            dt = time - previous_time
            if dt > 0:
                self.wait(dt)
            previous_time = time
            if message[index].isspace():
                continue
            self.add(LetterWork(letter=message[index], initial_position=self.initial_position(alpha),\
                initial_velocity=self.initial_velocity(alpha),\
                reference_colors=self.reference_colors(alpha)))

        last_exit_time = max(map(self.screen_exit_time, alphas)) - earliest_start
        self.wait(1 + last_exit_time - previous_time)

class StaggeredFireworkScene(FireworkScene):

    def arrival_time(self, alpha):
        return 5 + (len(message) - 1) * alpha

class CircularFireworkScene(FireworkScene):

    def final_position(self, alpha):
        alpha *= (1 - 1/len(message))
        return 1/2 * config.frame_y_radius * np.array([math.sin(alpha * 2 * math.pi), math.cos(alpha * 2 * math.pi), 0])

    def initial_position(self, alpha):
        return np.array([0, -config.frame_y_radius, 0])

class StaggeredCircularFireworkScene(CircularFireworkScene, StaggeredFireworkScene):
    pass

class SinusoidalFireworkScene(FireworkScene):

    def final_position(self, alpha):
        left_edge = -config.frame_x_radius + 1.5 * config.frame_width / (len(message) + 1)
        right_edge = -left_edge
        return np.array([interpolate(left_edge, right_edge, alpha), 1/2 * config.frame_y_radius * math.sin(alpha * 2 * math.pi), 0])

class StaggeredSinusoidalFireworkScene(SinusoidalFireworkScene, StaggeredFireworkScene):
    pass

class OddEvenNewYearScene(Scene):

    def construct(self):
        initial_spacing = np.linspace(-1/2 * config.frame_x_radius, 1/2 * config.frame_x_radius, len(message) + 2)
        final_spacing = np.linspace(-config.frame_x_radius, config.frame_x_radius, len(message) + 2)
        initial_velocity_x = (final_spacing - initial_spacing) / explosion_time

        rainbow = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, "#4B0082", "#EE82EE"], len(message) + 1)
        firework_colors = zip(rainbow, rainbow[1:])

        data = list(zip(message, initial_spacing[1:], initial_velocity_x[1:], firework_colors))

        for letter, start_x, v_x, reference_colors in data[1::2]:
            if letter.isspace():
                continue
            self.add(LetterWork(letter=letter, initial_position = start_x * RIGHT + config.frame_y_radius * DOWN,\
                 initial_velocity = v_x * RIGHT + initial_velocity_y * UP,\
                 reference_colors = reference_colors))
        self.wait(1)
        for letter, start_x, v_x, reference_colors in data[::2]:
            if letter.isspace():
                continue
            self.add(LetterWork(letter=letter, initial_position = start_x * RIGHT + config.frame_y_radius * DOWN,\
                 initial_velocity = v_x * RIGHT + initial_velocity_y * UP,\
                 reference_colors = reference_colors))
        self.wait(11)

class NewYearScene(Scene):
    
    def construct(self):

        initial_spacing = np.linspace(-1/2 * config.frame_x_radius, 1/2 * config.frame_x_radius, len(message) + 2)
        final_spacing = np.linspace(-config.frame_x_radius, config.frame_x_radius, len(message) + 2)
        initial_velocity_x = (final_spacing - initial_spacing) / explosion_time

        rainbow = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, "#4B0082", "#EE82EE"], len(message) + 1)
        firework_colors = zip(rainbow, rainbow[1:])

        for letter, start_x, v_x, reference_colors in zip(message, initial_spacing[1:], initial_velocity_x[1:], firework_colors):
            if letter.isspace():
                self.wait(1)
                continue
            self.add(LetterWork(letter=letter, initial_position = start_x * RIGHT + config.frame_y_radius * DOWN,\
                 initial_velocity = v_x * RIGHT + initial_velocity_y * UP,\
                 reference_colors = reference_colors))
            self.wait(1)
        self.wait(10)

class FireworkParticle(Dot):
    
    def __init__(self, initial_velocity, radius=0.02, **kwargs):
        super().__init__(radius=radius, **kwargs)
        self.velocity = initial_velocity
        self.add_updater(FireworkParticle.apply_gravity)

    def apply_gravity(self, dt):
        self.shift(self.velocity * dt)
        self.velocity += gravity * dt

class Firework(VGroup):
    
    def __init__(self, initial_position=ORIGIN, initial_velocity=UP, num_particles = 150, reference_colors = [WHITE], **kwargs):
        super().__init__(**kwargs)
        self.add(FireworkParticle(point=initial_position, initial_velocity=initial_velocity, **kwargs))
        self.initial_velocity = initial_velocity
        self.exploded = False
        self.num_particles = num_particles
        self.color_map = color_gradient(reference_colors, self.num_particles)
        self.add_updater(Firework.check_for_explosion)

    def get_random_velocity(self):
        return np.array([random.uniform(-1, 1), random.uniform(-1, 1), 0])

    def check_for_explosion(self, dt):
        if not self.exploded:
            launcher = self.submobjects[0]
            if launcher.velocity[1] <= 0:
                self.remove(launcher)
                self.add(*[FireworkParticle(point=launcher.get_center(), initial_velocity=self.get_random_velocity(), color=self.color_map[i]) for i in range(self.num_particles)])
                self.exploded = True

class LetterWork(Firework):

    def __init__(self, letter="O", **kwargs):
        super().__init__(**kwargs)
        self.letter = letter
        self._letter_mobject = Text(letter)[0]

    def get_random_velocity(self):
        return self._letter_mobject.point_from_proportion(random.random())  + self.initial_velocity[0] * RIGHT
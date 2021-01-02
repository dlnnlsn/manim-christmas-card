from manim import *
import random

explosion_height = 3/4 * config.frame_height
explosion_time = 5

gravity_y = -2 * explosion_height / explosion_time**2
initial_velocity_y = -gravity_y * explosion_time

gravity = gravity_y * UP

message = "Happy New Year!"

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
        return self._letter_mobject.point_from_proportion(random.random())
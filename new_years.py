from manim import *

#make it take 10s for a particle to fall between the top and bottom of the screen
gravity = 2 * config.frame_height / 100 * DOWN

class NewYearScene(Scene):
    
    def construct(self):
        firework = Firework(initial_position = ORIGIN, initial_velocity = -9 * gravity)
        firework.to_edge(DOWN, buff=0)
        self.add(firework)
        self.wait(20)

class FireworkParticle(Dot):
    
    def __init__(self, initial_velocity, **kwargs):
        super().__init__(**kwargs)
        self.velocity = initial_velocity
        self.add_updater(FireworkParticle.apply_gravity)

    def apply_gravity(self, dt):
        self.shift(self.velocity * dt)
        self.velocity += gravity * dt

class Firework(VGroup):
    
    def __init__(self, initial_position, initial_velocity, **kwargs):
        super().__init__(**kwargs)
        self.add(FireworkParticle(point=initial_position, initial_velocity=initial_velocity, **kwargs))
        self.add_updater(Firework.apply_gravity)
        self.exploded = False

    def apply_gravity(self, dt):
        if not self.exploded:
            launcher = self.submobjects[0]
            if launcher.velocity[1] <= 0:
                self.remove(launcher)
                self.add(*[FireworkParticle(point=launcher.get_center(), initial_velocity=np.random.uniform(-1, 1, 3)) for _ in range(100)])
                self.exploded = True
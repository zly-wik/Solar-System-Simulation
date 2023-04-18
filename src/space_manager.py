"""Module for core simulation classes."""
import pygame

from gravity import GravityManager, GravityObject


class SpaceManager(object):
    """Main class used for rendering and simulating physics and rendering."""

    def __init__(self) -> None:
        """Initialize Pygame and basic objects."""
        self.gravity = GravityManager()

        pygame.init()
        pygame.display.set_caption('Solar System')
        self.window = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.dt = 0

        pos1 = pygame.Vector2(
            self.window.get_width(),
            self.window.get_height(),
        ) / 2
        self.obj1 = GravityObject(pos1, 15000.0)

        self.obj2 = GravityObject(
            position=pygame.Vector2(0, 0),
            mass=70.0,
            active=False,
        )

        self.gravity.add_object_to_pool(self.obj1)
        self.gravity.add_object_to_pool(self.obj2)

    def main_loop(self):
        """Run simulation main loop."""
        running = True
        while running:
            running = self.get_events()
            self.draw()
            self.gravity.apply_gravity(self.dt)

            self.dt = self.clock.tick(60) / 1000

    def get_keydown_events(self, event):
        """Get user inputs."""
        if event.key == pygame.K_ESCAPE:
            return False
        if event.key == pygame.K_2:
            self.obj1.velocity = pygame.Vector2(0, 0)
            self.obj1.position = pygame.Vector2(
                self.window.get_width(),
                self.window.get_height(),
            ) / 2
            self.obj2.active = True
            self.obj2.velocity = pygame.Vector2(0, 0)
            self.obj2.position = pygame.Vector2(
                *pygame.mouse.get_pos(),
            )
        if event.key == pygame.K_SPACE:
            self.obj2.velocity += pygame.Vector2(
                pygame.Vector2(
                    *pygame.mouse.get_pos(),
                ) - self.obj2.position,
            ).clamp_magnitude(10.0) * 10.0
        if event.key == pygame.K_q:
            self.obj2.active = False
        if event.key == pygame.K_DOWN:
            self.obj2.mass -= 10.0 if self.obj2.mass > 10 else 0
        if event.key == pygame.K_UP:
            self.obj2.mass += 10.0

    def get_events(self):
        """Get events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.get_keydown_events(event)

        return True

    def draw_objects(self):
        """Draw all active gravity objects."""
        for obj in self.gravity.get_objects_from_pool():
            if obj.active:
                pygame.draw.circle(
                    self.window,
                    color='red',
                    center=obj.position,
                    radius=30.0,
                )

    def draw(self):
        """Draw new pygame frame."""
        self.window.fill('darkblue')
        self.draw_objects()

        pygame.display.flip()

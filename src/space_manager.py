"""Module for core simulation classes."""
import pygame as pg
from pygame import Vector2

from game_object import GameObject
from gravity import GravityManager


class ObjectPool(object):
    """Object Pool for used GameObjects."""

    def __init__(self) -> None:
        """Initialize object pool parameters."""
        self.gravity = GravityManager()
        self.object_pool: list[GameObject] = []

    def add_object_to_pool(self, obj: GameObject) -> bool:
        """Add game object to pool."""
        if obj not in self.object_pool:
            self.object_pool.append(obj)

            gravity = obj.__dict__.get('gravity_object')
            if gravity:
                self.gravity.add_object_to_pool(gravity)

    def get_objects_from_pool(self) -> list[GameObject]:
        """Return list of pool objects."""
        return self.object_pool


class SpaceManager(object):
    """Main class used for rendering and simulating physics and rendering."""

    def __init__(self) -> None:
        """Initialize Pygame and basic objects."""
        self.object_pool = ObjectPool()

        pg.init()
        pg.display.set_caption('Solar System')
        self.window = pg.display.set_mode((1280, 720))
        self.clock = pg.time.Clock()
        self.dt = 0

        pos1 = pg.Vector2(
            self.window.get_width(),
            self.window.get_height(),
        ) / 2
        self.obj1 = GameObject(
            position=pos1,
            radius=35.0,
            color='yellow',
            active=True,
        )

        self.obj2 = GameObject(
            position=Vector2(0, 0),
            radius=10.0,
            color='red',
            active=False,
        )

        self.obj1.initialize_physics(mass=15000.0)
        self.obj2.initialize_physics(
            mass=70.0,
            velocity=Vector2(35.0),
            active=False,
        )

        self.object_pool.add_object_to_pool(self.obj1)
        self.object_pool.add_object_to_pool(self.obj2)

    def main_loop(self) -> None:
        """Run simulation main loop."""
        running = True
        while running:
            running = self.get_events()
            self.draw()
            self.object_pool.gravity.apply_gravity(self.dt)

            self.dt = self.clock.tick(60) / 1000

    def get_keydown_events(self, event) -> bool:
        """Get user inputs."""
        if event.key == pg.K_ESCAPE:
            return False
        if event.key == pg.K_2:
            self.obj1.gravity_object.velocity = pg.Vector2(0, 0)
            self.obj1.gravity_object.position = pg.Vector2(
                self.window.get_width(),
                self.window.get_height(),
            ) / 2
            self.obj2.gravity_object.active = True
            self.obj2.active = True
            self.obj2.gravity_object.velocity = pg.Vector2(0, 0)
            self.obj2.position = pg.Vector2(
                *pg.mouse.get_pos(),
            )
        if event.key == pg.K_SPACE:
            self.obj2.gravity_object.velocity += pg.Vector2(
                pg.Vector2(
                    *pg.mouse.get_pos(),
                ) - self.obj2.gravity_object.position,
            ).clamp_magnitude(10.0) * 10.0
        if event.key == pg.K_q:
            self.obj2.gravity_object.active = False
            self.obj2.active = False
        if event.key == pg.K_DOWN:
            self.obj2.gravity_object.mass -= 10.0 if self.obj2.gravity_object.mass > 10 else 0
        if event.key == pg.K_UP:
            self.obj2.gravity_object.mass += 10.0

        return True

    def get_events(self) -> bool:
        """Get events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                return self.get_keydown_events(event)

        return True

    def draw_objects(self) -> None:
        """Draw all active gravity objects."""
        for obj in self.object_pool.get_objects_from_pool():
            if obj.active:
                pg.draw.circle(
                    self.window,
                    color=obj.color,
                    center=obj.position,
                    radius=obj.radius,
                )

    def draw(self) -> None:
        """Draw new pg frame."""
        self.window.fill('darkblue')
        self.draw_objects()

        pg.display.flip()

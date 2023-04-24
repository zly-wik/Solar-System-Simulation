"""Gravity module used for calculating gravity of objects."""
import pygame

G = 6.6743


class GravityObject(object):
    """Gravity object class used as base class for all gravity objects."""

    def __init__(
        self,
        position: pygame.Vector2,
        mass: float | None = 10.0,
        velocity: pygame.Vector2 | None = None,
        active: bool | None = True,
    ) -> None:
        """Gravity object setup with basics physics parameters."""
        self.position: pygame.Vector2 = position
        self.mass: float = mass
        self.velocity: pygame.Vector2 = velocity or pygame.Vector2(0, 0)
        self.active = active

    def update_velocity(self, velocity_delta) -> None:
        """Update object velocity by adding velocity delta."""
        if not self.active:
            return
        self.velocity += velocity_delta

    def apply_velocity(self) -> None:
        """Apply velocity to object by updating position."""
        if not self.active:
            return
        self.position += self.velocity / self.mass


class GravityManager(object):
    """Gravity Manager object used for managing all active gravity objects."""

    def __init__(self) -> None:
        """Initialize object pool."""
        self.object_pool: list[GravityObject] = []

    def add_object_to_pool(self, obj) -> bool:
        """Add gravity object to pool."""
        if isinstance(obj, GravityObject):
            self.object_pool.append(obj)
            return True

        return False

    def get_objects_from_pool(self) -> list[GravityObject]:
        """Get all objects from pool."""
        return self.object_pool

    def apply_gravity(self, dt: float) -> None:
        """Apply gravity to all object in object_pool.

        Nested loops used for apply gravity for every object
        in relation with all others.

        Will be changed in future to ignore far objects (performance).
        """
        for obj in self.object_pool:
            for interact_object in self.object_pool:
                if not self.should_apply_gravity(obj, interact_object):
                    continue

                vel: pygame.Vector2 = self.calculate_velocity_delta(
                    obj,
                    interact_object,
                    dt,
                )

                obj.update_velocity(velocity_delta=vel)
                obj.apply_velocity()

    def should_apply_gravity(
        self,
        obj1: GravityObject,
        obj2: GravityObject,
    ) -> bool:
        """Decide if gravity should be applied to these objects."""
        return obj1 != obj2 and obj1.active and obj2.active

    def calculate_velocity_delta(
        self,
        obj1: GravityObject,
        obj2: GravityObject,
        dt: float,
    ) -> pygame.Vector2:
        """Calculate velocity delta between 2 gravity objects."""
        distance: float = obj1.position.distance_to(
            obj2.position,
        )

        if distance <= 0:
            return None

        direction: pygame.Vector2 = (
            obj2.position - obj1.position
        ).normalize()

        force: float = (
            G * obj1.mass * obj2.mass / distance**2
        )

        return direction * force * dt

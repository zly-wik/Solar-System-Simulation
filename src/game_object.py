"""Game object module used for rendering objects."""
from pygame import Color, Vector2

from gravity import GravityObject


class StaticGameObject(object):
    """Static Game Object class used for representing objects."""

    def __init__(
        self,
        position: Vector2,
        radius: float,
        color: Color,
        active: bool | None = True,
    ) -> None:
        """Initialize static game object.

        Object represented without physics and collisions.
        """
        self.position = position
        self.radius: float = radius
        self.color: Color = color
        self.active: bool = active


class GameObject(StaticGameObject):
    """Game object class representing objects with gravity."""

    def __init__(
        self,
        position: Vector2,
        radius: float,
        color: Color,
        active: bool | None = True,
    ) -> None:
        """Initialize game object.

        Object represented with physics and/or collisions.
        """
        super().__init__(position, radius, color, active)

        self.gravity_object = GravityObject(position)

    def initialize_physics(
        self,
        mass: float,
        velocity: Vector2 | None = None,
        active: bool | None = True,
    ) -> None:
        """Update physics in gravity object."""
        self.gravity_object.mass = mass
        self.gravity_object.velocity = velocity or Vector2(0, 0)
        self.gravity_object.active = active

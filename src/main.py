"""Entrypoint of this project."""
import pygame

from space_manager import SpaceManager


def main():
    """Program entrypoint."""
    sm: SpaceManager = SpaceManager()
    sm.main_loop()

    pygame.quit()


if __name__ == '__main__':
    main()

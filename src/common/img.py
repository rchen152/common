"""Image handling."""

import abc
import enum
import inspect
import os
import pygame


class PathType(enum.Enum):
    LOCAL = enum.auto()  # load from a local img/ directory
    COMMON = enum.auto()  # load from common/img/


class Factory(abc.ABC):

    def __init__(self, screen):
        self._screen = screen

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def collidepoint(self, pos):
        pass


class RectFactory(Factory):
    """A factory bounded by a rectangle."""

    RECT: pygame.Rect

    def collidepoint(self, pos):
        return self.RECT.collidepoint(pos)

    def move(self, delta):
        self.RECT = self.RECT.move(delta)


def _get_img_dir(path_type):
    if path_type is PathType.LOCAL:
        for frame in inspect.stack():
            if os.path.basename(frame.filename) != 'img.py':
                ref_file = frame.filename
                break
        else:
            assert False, 'no local caller found'
    else:
        assert path_type is PathType.COMMON
        ref_file = __file__
    return os.path.join(os.path.dirname(ref_file), 'img')


class PngFactory(RectFactory):

    def __init__(self, name, screen, position=(0, 0), shift=(0, 0),
                 path_type=PathType.LOCAL):
        """Initializer for a png image.

        Args:
          name: The name of the image without the png extension.
          screen: The screen to draw the image on.
          position: The position of the image's top-left corner.
          shift: A tuple of factors of the width and height to shift the
            position by.
        """
        super().__init__(screen)
        path = os.path.join(_get_img_dir(path_type), f'{name}.png')
        self._img = pygame.image.load(path).convert_alpha()
        pos = (position[0] + self._img.get_width() * shift[0],
               position[1] + self._img.get_height() * shift[1])
        self.RECT = pygame.Rect(pos, self._img.get_size())

    def draw(self):
        self._screen.blit(self._img, self.RECT.topleft)


def load(*args, factory=PngFactory, **kwargs):
    return factory(*args, **kwargs)

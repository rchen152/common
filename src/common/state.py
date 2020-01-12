"""Game state."""

import abc
import pygame
from pygame.locals import *
from . import color
from . import img


RECT = pygame.Rect(0, 0, 1024, 576)


def keypressed(event, key, mod=None):
    return (event.type == KEYDOWN and event.key == key and
            (mod is None or event.mod & mod))


class GameState(abc.ABC):
    """Base class for tracking game state.

    run() checks the event queue in a loop until a quit event is received. For
    each event, every handle_* method is called until the event is consumed. A
    handler reports that it consumed an event by returning True.
    """

    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.draw()
        self._event_handlers = [
            getattr(self, x) for x in dir(self) if x.startswith('handle_')]

    @abc.abstractmethod
    def draw(self):
        pass

    def cleanup(self):
        pass

    def handle_quit(self, event):
        if event.type == QUIT or keypressed(event, K_c, KMOD_CTRL):
            self.active = False
            return True
        return False

    def handle_fullscreen(self, event):
        if not keypressed(event, K_F11):
            return False
        if self.screen.get_flags() & FULLSCREEN:
            pygame.display.set_mode(RECT.size)
        else:
            pygame.display.set_mode(RECT.size, FULLSCREEN)
        self.draw()
        return True

    def run(self):
        while self.active:
            for event in pygame.event.get():
                for handle in self._event_handlers:
                    consumed = handle(event)
                    if consumed:
                        break
        self.cleanup()


class TitleCard(GameState):

    _TIMED_QUIT = pygame.USEREVENT
    _DISPLAY_TIME_MS = 5000

    def __init__(self, screen):
        self._title_card_img = img.load('title_card', screen)
        super().__init__(screen)
        pygame.time.set_timer(self._TIMED_QUIT, self._DISPLAY_TIME_MS)

    def draw(self):
        self.screen.fill(color.BLUE)
        self._title_card_img.draw()
        pygame.display.update()

    def handle_quit(self, event):
        if event.type == self._TIMED_QUIT:
            self.active = False
            return True
        return super().handle_quit(event)

    def cleanup(self):
        pygame.time.set_timer(self._TIMED_QUIT, 0)

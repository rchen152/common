"""Tests for common.state."""

import pygame
from pygame.locals import *

import unittest
import unittest.mock

from common import state
from common import test_utils


class MockGame(state.GameState):

    def __init__(self, screen):
        self.drawn = 0
        self.clean = False
        super().__init__(screen)

    def draw(self):
        self.drawn += 1

    def cleanup(self):
        self.clean = True


class GameStateTest(unittest.TestCase):

    def setUp(self):
        self.state = MockGame(test_utils.MockScreen())

    def mock_set_mode(self, size, fullscreen=False):
        del size  # unused
        self.state.screen.fullscreen = fullscreen

    def test_abstract(self):
        with self.assertRaises(TypeError):
            # pytype: disable=not-instantiable
            state.GameState(test_utils.MockScreen())
            # pytype: enable=not-instantiable

    def test_basic(self):
        self.assertTrue(self.state.active)
        self.assertEqual(self.state.drawn, 1)

    def test_quit_x(self):
        self.assertTrue(self.state.active)
        self.state.handle_quit(test_utils.MockEvent(QUIT))
        self.assertFalse(self.state.active)

    def test_quit_q(self):
        self.assertTrue(self.state.active)
        self.state.handle_quit(
            test_utils.MockEvent(KEYDOWN, key=K_c, mod=KMOD_CTRL))
        self.assertFalse(self.state.active)

    def test_fullscreen(self):
        self.state.screen.fullscreen = False
        with unittest.mock.patch.object(
                pygame.display, 'set_mode', self.mock_set_mode):
            self.state.handle_fullscreen(
                test_utils.MockEvent(KEYDOWN, key=K_F11))
        self.assertTrue(self.state.screen.fullscreen)
        self.assertEqual(self.state.drawn, 2)

    def test_unfullscreen(self):
        self.state.screen.fullscreen = True
        with unittest.mock.patch.object(
                pygame.display, 'set_mode', self.mock_set_mode):
            self.state.handle_fullscreen(
                test_utils.MockEvent(KEYDOWN, key=K_F11))
        self.assertFalse(self.state.screen.fullscreen)
        self.assertEqual(self.state.drawn, 2)

    def test_run(self):
        self.state.screen.fullscreen = False
        with unittest.mock.patch.object(
                pygame.display, 'set_mode', self.mock_set_mode):
            with unittest.mock.patch.object(pygame.event, 'get') as mock_get:
                mock_get.return_value = [
                    test_utils.MockEvent(KEYDOWN, key=K_F11),
                    test_utils.MockEvent(KEYDOWN, key=K_F11),
                    test_utils.MockEvent(KEYDOWN, key=K_F11),
                    test_utils.MockEvent(KEYDOWN, key=K_c, mod=KMOD_CTRL),
                ]
                self.state.run()
        self.assertTrue(self.state.screen.fullscreen)
        self.assertEqual(self.state.drawn, 4)
        self.assertFalse(self.state.active)

    def test_cleanup(self):
        self.assertFalse(self.state.clean)
        with unittest.mock.patch.object(pygame.event, 'get') as mock_get:
            mock_get.return_value = [test_utils.MockEvent(QUIT)]
            self.state.run()
        self.assertTrue(self.state.clean)


class TitleCardTest(test_utils.ImgTestCase):

    def test_init(self):
        with test_utils.patch('pygame.display', autospec=True):
            with test_utils.patch('pygame.transform', autospec=True):
                state.TitleCard(self.screen)


if __name__ == '__main__':
    unittest.main()

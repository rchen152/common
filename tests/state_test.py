"""Tests for common.state."""

import unittest

from common import state
from common import test_utils


class TitleCardTest(test_utils.ImgTestCase):

    def test_init(self):
        with test_utils.patch('pygame.display', autospec=True):
            with test_utils.patch('pygame.transform', autospec=True):
                state.TitleCard(self.screen)


if __name__ == '__main__':
    unittest.main()

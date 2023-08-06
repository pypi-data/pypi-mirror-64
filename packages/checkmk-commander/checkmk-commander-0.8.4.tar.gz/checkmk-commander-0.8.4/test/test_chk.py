
#https://python-packaging.readthedocs.io/en/latest/testing.html

from unittest import TestCase

import checkmkcommander

class TestChk(TestCase):
    def test_is_string(self):
        s = funniest.joke()
        self.assertTrue(isinstance(s, basestring))

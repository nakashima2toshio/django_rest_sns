# TestCase description Template
import os
from unittest import TestCase


class APlusTestCase(TestCase):

    def setUp(self) -> None:
        self.answer = 5
        print('setUp-->', __class__.__name__)

    def tearDown(self):
        print('tearDown-->', __class__.__name__)

    def test_a_plus(self):
        print('test-1a')
        a = 5
        assert a is self.answer


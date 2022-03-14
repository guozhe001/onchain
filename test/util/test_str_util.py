from unittest import TestCase

from util import str_util


class Test(TestCase):
    def test_contains(self):
        self.assertFalse(str_util.contains("hello", "hi"))

    def test_contains_true(self):
        self.assertTrue(str_util.contains("hello", "hell"))

    def test_contains_true1(self):
        self.assertTrue(str_util.contains("hello", "llo"))

    def test_for(self):
        words = ["a", "b", "c"]
        nums = [1, 2, 3]
        for word, num in zip(words, nums):
            print(word, num)

#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock

from tmc import points
from tmc.utils import load, get_out, patch_helper, spy_decorator

 = load('src.', '')
main = load(module_name, "main")
ph = patch_helper(module_name)


@points('p01-01.1')
class TestDnaToRna(unittest.TestCase):

    
    def test_first(self):
        self.assertEqual("", "")


if __name__ == '__main__':
    unittest.main()
    

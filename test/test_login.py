# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:57:12 2019

@author: xiong
"""

import unittest
import sys
sys.path.append("..")
from src.login import Login
login = Login(2109236844, b"123456xx")

# MD51(b'123456xx')
# 6D 43 EB D3 1B 9E 35 25 37 61 77 7E BA E5 D9 CF
# MD51 + hex(用户名)
# 6D 43 EB D3 1B 9E 35 25 37 61 77 7E BA E5 D9 CF
# 00 00 00 00 7D B8 66 6C
# MD52:
# B3 E2 EA AB C4 9B 6D 9F 6F DB C4 CF B8 E5 58 39
class TestLogin(unittest.TestCase):
    """Test src/login.py"""
    def test_get_md2(self):
        """Test methodshow_user()"""
        #self.login = Login(2109236844, b"123456xx")
        self.assertEqual("b3e2eaabc49b6d9f6fdbc4cfb8e55839", login.get_md2())

if __name__ == '__main__':
    unittest.main()
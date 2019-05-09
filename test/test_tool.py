# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:32:12 2019

@author: xiong
"""

import unittest
import sys
sys.path.append("..")
from src.tool import Tool
tool = Tool()
class TestTool(unittest.TestCase):
    """Test src/tool.py"""
    def test_md5(self):
        """Test method md5()"""
        self.assertEqual("b3e2eaabc49b6d9f6fdbc4cfb8e55839", tool.md5(2109236844, b"123456xx"))
    def test_get_host_by_name(self):
        self.assertEqual("61.151.180.166", tool.get_host_by_name("61.151.180.166"))
        self.assertEqual("61.151.180.166", tool.get_host_by_name("sz6.tencent.com")) # sz.tencent.com,sz{2-9}.tencent.com
if __name__ == '__main__':
    unittest.main()
    v = '023709082536367DB8666C030000000101010000681C30000000752406735B804AF4861322F9A09E938E5AC2CD0E0A7C9018AA16B16400AA6253BED51F86A2C6DDB1C7E85B5444DDA02B57DB7E324EF798584CE703BFB8FCC5A0F6586A5CF2D6DCF6151B2EC16CB7311EB9EE87D24D32217B7779E9BB0184D4B2ADC8B0BEA6CE776629ED8AEBDE8B3DDA4BACE8AFEB2E6CC803'
    v = v.lower()
    v = v.encode('utf-8')
    print("v", v,len(v))
    app = []
    b = b''
    for i in range(0,len(v),2):
        v1 = v[i:i+2].decode("utf-8")
        b += bytes([int("0x"+v1,16)])
        app.append(v1)
    print(app)
    print(b,len(b))
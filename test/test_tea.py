# -*- coding: utf-8 -*-
"""
Created on Tue May  7 18:06:38 2019

@author: xiong
"""

import unittest
import sys
sys.path.append("..")
from src.tea import Tea
tea = Tea()
class TestTea(unittest.TestCase):
    """Test src/tea.py"""
    def test_format_key(self):
        """Test method format_key()"""
        #array = [1333436914,2272652757,564238896,517702433]
        #self.assertEqual(array, tea.format_key(b"4F7AA1F28775EDD521A19A301EDB8321"))
        array2 = [3980167545, 461067553, 3328928192, 3526830759]
        self.assertEqual(array2, tea.format_key(b"ED3C89791B7B5521C66B69C0D2372AA7"))
    def test_filling(self):
        """"""
        inner = '0018001600010000045300000001000015857DB8666C000000000309000800013D97B4AB0001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA'.lower().encode('utf-8')
        filling_inner = '010101010018001600010000045300000001000015857DB8666C000000000309000800013D97B4AB0001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA00000000000000'.lower().encode('utf-8')
        filling_result = tea.filling(inner,1)
        self.assertEqual(filling_inner,filling_result[0])
        inner2 = '0018001600010000045300000001000015857DB8666C000000000309000800013D97B5610001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA'.lower().encode('utf-8')
        filling_inner2 = '010101010018001600010000045300000001000015857DB8666C000000000309000800013D97B5610001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA00000000000000'.lower().encode('utf-8')
        filling_result2 = tea.filling(inner2,1)
        self.assertEqual(filling_inner2,filling_result2[0])
    @unittest.skip(u"强制跳过")
    def test_code(self):
        """Test method code(self, inner, inOffset, inPos, Out, outOffset, outPos, key)"""
        tin = '010101010018001600010000045300000001000015857DB8666C000000000309000800013D97E2A90001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA00000000000000'.lower().encode('utf-8')
        tkey ='A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        ts = tea.code(tin,0,0,b'',0,0,tkey)
        self.assertEqual(tin,ts[0])
        tValue = 'E0D7699C3630A898'.lower().encode('utf-8')
        self.assertEqual(tValue,ts[1])
        # print(ts[0])
        ts = tea.code(ts[0],0,8,ts[1],0,8,tkey)
        tin2 = '0101010100180016E0D6699C3263A8980001000015857DB8666C000000000309000800013D97E2A90001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA00000000000000'.lower().encode('utf-8')
        tValue2 = 'E0D7699C3630A898FF5EFDBE7A003748'.lower().encode('utf-8')
        self.assertEqual(tin2.decode('utf-8'),ts[0].decode('utf-8'))
        self.assertEqual(tValue2,ts[1])
        # 循环测试
    def test_for_code(self):
        """Test method code() foreach"""
        tin = '010101010018001600010000045300000001000015857DB8666C000000000309000800013D97B5610001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA00000000000000'.lower().encode('utf-8')
        tkey = 'A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        array2 = b''
        for i in range(0,int(len(tin)/2),8):
            tin,array2 = tea.code(tin,0,i,array2,0,i,tkey)
            #print(i,"tin",tin,"array2:",array2)
        tValue = 'E0D7699C3630A898FF5EFDBE7A003748743400C9C63DB85493C6267AC8A67C8777EA7D30A4192FF1AD6F8299F5F7A01C267F78220DD054E48C8B7E39063F0E9BAE40F24577243082D49D725E4FFFA6945AA337A8244285517626A8B43B89700928A83066BF08AC59'.lower().encode('utf-8')
        self.assertEqual(tValue,array2)
    def test_encrypt(self):
        inner = '0018001600010000045300000001000015857DB8666C000000000309000800013D97B5610001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA'.lower().encode('utf-8')
        key = 'A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        result = tea.encrypt(inner, key,1)
        should_result = 'E0D7699C3630A898FF5EFDBE7A003748743400C9C63DB85493C6267AC8A67C8777EA7D30A4192FF1AD6F8299F5F7A01C267F78220DD054E48C8B7E39063F0E9BAE40F24577243082D49D725E4FFFA6945AA337A8244285517626A8B43B89700928A83066BF08AC59'.lower().encode('utf-8')
        self.assertEqual(should_result,result)
    #@unittest.skip(u"强制跳过")
    def test_decrypt(self):
        inner = 'E0D7699C3630A898FF5EFDBE7A003748743400C9C63DB85493C6267AC8A67C87D9A6DF7EC18DEAE2193318782836D4E54D83629A59FD0308778B4048BEEF54E5FBBDFF7FE09B790F7C72833BA7547FA363B2CE13C073E3009CFAD0B819ACFB1644080396A39EC6EF'.lower().encode('utf-8')
        key = 'A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        tValue= b'0018001600010000045300000001000015857db8666c000000000309000800013d97e2a60001003600120002000100000001000000000000000000000114001d01020019027828167c9ef3b75a7b5aefa23010ec0c4687707631a788ea'
        result = tea.decrypt(inner,key)
        self.assertEqual(tValue,result)
    def test_decode(self):
        """Test method code(self, inner, inOffset, inPos, Out, outOffset, outPos, key)"""
        tin = 'E0D7699C3630A898FF5EFDBE7A003748743400C9C63DB85493C6267AC8A67C871DD83E661F9B4BA0F29474DC702F7683462D4ABC6E2FDC30CA7F278A863384129CB42AFCC8628AD60811B53D672C3BAA0C015A3709C815050F5D3450DF4AB5672A16DEE056A92B12'.lower().encode('utf-8')
        tkey ='A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        ts = tea.decode(tin,0,0,b'',0,0,tkey)
        self.assertEqual(tin,ts[0])
        tValue = '0101010100180016'.lower().encode('utf-8')
        self.assertEqual(tValue,ts[1])
        tValue2 = '0101010100180016E0D6699C3263A898'.lower().encode('utf-8')
        ts2 = tea.decode(tin,0,8,tValue,0,8,tkey)
        self.assertEqual(tValue2,ts2[1])
    def test_for_decode(self):
        tin = 'E0D7699C3630A898FF5EFDBE7A003748743400C9C63DB85493C6267AC8A67C87D9A6DF7EC18DEAE2193318782836D4E54D83629A59FD0308778B4048BEEF54E5FBBDFF7FE09B790F7C72833BA7547FA363B2CE13C073E3009CFAD0B819ACFB1644080396A39EC6EF'.lower().encode('utf-8')
        tkey ='A882182C58040751E646866D51928CC3'.lower().encode('utf-8')
        array2 = b''
        for i in range(0,int(len(tin)/2),8):
            tin,array2 = tea.decode(tin,0,i,array2,0,i,tkey)
        #print("循环结果",array2)
        array2_content = array2[0:16]
        array2_center = b''
        for i in range(8,int(len(tin)/2)):
            a1 = tea.hex_to_int(array2[i*2:i*2+2])
            a2 = tea.hex_to_int(tin[(i-8)*2:(i-8)*2+2])
            array2_center  += tea.int_to_hex(a1^a2)
        array2_content= array2_content + array2_center
        #print("修改array2_content",array2_content)
        num = tea.hex_to_int(array2_content[0:2])&7
        #print("num",num,array2_content[num*2+6:-14])
        length = len(tin) - num*2 - 20
        #print("num",num,)
        tValue= b'0018001600010000045300000001000015857db8666c000000000309000800013d97e2a60001003600120002000100000001000000000000000000000114001d01020019027828167c9ef3b75a7b5aefa23010ec0c4687707631a788ea'
        self.assertEqual(tValue,array2_content[num*2+6:num*2+6+length])

    def test_convert_int2bytes(self):
        n1 = 3772213660
        n2 = 909158552
        tValue = 'E0D7699C3630A898'.lower().encode('utf-8')
        self.assertEqual(tValue,tea.convert_int2bytes(n1) + tea.convert_int2bytes(n2))
if __name__ == '__main__':
    unittest.main()   
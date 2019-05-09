# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:41:34 2019
/**
 * 加密解密QQ消息的工具类. QQ消息的加密算法是一个16次的迭代过程，并且是反馈的，每一个加密单元是8字节，输出也是8字节，密钥是16字节
 * 我们以prePlain表示前一个明文块，plain表示当前明文块，crypt表示当前明文块加密得到的密文块，preCrypt表示前一个密文块
 * f表示加密算法，d表示解密算法 那么从plain得到crypt的过程是: crypt = f(plain &circ; preCrypt) &circ;
 * prePlain 所以，从crypt得到plain的过程自然是 plain = d(crypt &circ; prePlain) &circ;
 * preCrypt 此外，算法有它的填充机制，其会在明文前和明文后分别填充一定的字节数，以保证明文长度是8字节的倍数
 * 填充的字节数与原始明文长度有关，填充的方法是:
 * 
 * <pre>
 * <code> * 
 *      ------- 消息填充算法 ----------- 
 *      a = (明文长度 + 10) mod 8
 *      if(a 不等于 0) a = 8 - a;
 *      b = 随机数 &amp; 0xF8 | a;              这个的作用是把a的值保存了下来
 *      plain[0] = b;                     然后把b做为明文的第0个字节，这样第0个字节就保存了a的信息，这个信息在解密时就要用来找到真正明文的起始位置
 *      plain[1 至 a+2] = 随机数 &amp; 0xFF;    这里用随机数填充明文的第1到第a+2个字节
 *      plain[a+3 至 a+3+明文长度-1] = 明文; 从a+3字节开始才是真正的明文
 *      plain[a+3+明文长度, 最后] = 0;       在最后，填充0，填充到总长度为8的整数为止。到此为止，结束了，这就是最后得到的要加密的明文内容
 *      ------- 消息填充算法 ------------ *   
 * </code>
 * </pre> 
 */
@author: xiong
"""
import random
#import copy
class Tea:
    '''
    QQ tea算法 python实现
    '''
    def __init__(self):
        print("Tea")
        self.__name = 'Tea 学习'
    def code(self, inner, inOffset, inPos, Out, outOffset, outPos, key):
        """method code() 根据已有内容，输入会一直修改，而out每次都是新的"""
        if outPos > 0:
            inner_start = inner[0:(outOffset + outPos)*2]
            inner_body = inner[(outOffset + outPos)*2:(outOffset + outPos)*2+16]
            out_body = Out[(outOffset + outPos)*2 -16:(outOffset + outPos)*2]
            inner_end = inner[(outOffset + outPos)*2+16:]
            inner_center = b''
            for i in range(8):
                inner_1 = inner_body[i*2:i*2+2]
                out_1 = out_body[i*2:i*2+2]
                out_value = self.hex_to_int(inner_1)^self.hex_to_int(out_1)
                inner_center += self.int_to_hex(out_value)
            inner = inner_start + inner_center + inner_end
            #print("strat",inner_start)
            #print("cent",inner_center)
            #print("end",inner_end)
            #print(inner)
        array  = self.format_key(key) # int 4 
        #print(array)
        num = self.convert_bytes2int(inner,(outOffset + outPos)*2)
        num2 = self.convert_bytes2int(inner,(outOffset + outPos)*2 + 8)
        num3 = 0
        num4 = 2654435769
        #print("num:",num," num2:",num2," num3:",num3," num4:",num4)
        for i in range(16):
            num3 += num4
            num3 %= 4294967296 
            num += ((num2 << 4) + array[0]) ^ (num2 + num3) ^ ((num2 >> 5) + array[1])
            num %= 4294967296 
            num2 += ((num << 4) + array[2]) ^ (num + num3) ^ ((num >> 5) + array[3])
            num2 %= 4294967296 
            #print("num:",num," num2:",num2," num3:",num3)
        #print("num:",num," num2:",num2," num3:",num3," num4:",num4)
        get_num = self.convert_int2bytes(num) + self.convert_int2bytes(num2)
        if inPos > 0:
            out_1 = get_num
            inner_1 = inner[(inOffset + inPos)*2 - 16:(inOffset + inPos)*2]
            get_out = b''
            #print(get_num,inner_1)
            for i in range(8):
                inner_2 = inner_1[i*2:i*2+2]
                out_2 = out_1[i*2:i*2+2]
                out_value = self.hex_to_int(out_2)^self.hex_to_int(inner_2)
                get_out += self.int_to_hex(self.hex_to_int(inner_2)^self.hex_to_int(out_2))
            get_num = get_out
            #print(get_num)
        Out += get_num
        return inner,Out
    def decode(self, inner, inOffset, inPos, Out, outOffset, outPos, key):
        if outPos > 0:
            inner_body = inner[(outOffset + outPos)*2:(outOffset + outPos)*2+16]
            out_body = Out[(outOffset + outPos)*2 -16:(outOffset + outPos)*2]
            # print("123",inner_body,out_body)
            inner_center = b''
            for i in range(8):
                inner_1 = inner_body[i*2:i*2+2]
                out_1 = out_body[i*2:i*2+2]
                out_value = self.hex_to_int(inner_1)^self.hex_to_int(out_1)
                inner_center += self.int_to_hex(out_value)
            get_num = inner_center
            #print("strat",inner_start)
        else:
            get_num = inner[inPos*2:(inPos*2)+16]
        #print(inner)
        # print("getnum:",get_num)
        array  = self.format_key(key) # int 4 
        #print(array)
        num = self.convert_bytes2int(get_num,0)
        num2 = self.convert_bytes2int(get_num,8)
        num3 = 3816266640
        num4 = 2654435769
        # print("开始num:",num," num2:",num2," num3:",num3," num4:",num4)
        for i in range(16):
            num2 -= ((num << 4) + array[2]) ^ (num + num3) ^ ((num >> 5) + array[3])
            num2 %= 4294967296 
            num -= ((num2 << 4) + array[0]) ^ (num2 + num3) ^ ((num2 >> 5) + array[1])
            num %= 4294967296 
            num3 -= num4
            num3 %= 4294967296 
            #print("num:",num," num2:",num2," num3:",num3)
        # print("num:",num," num2:",num2," num3:",num3," num4:",num4)
        get_num = self.convert_int2bytes(num) + self.convert_int2bytes(num2)
        Out += get_num
        return inner,Out
    def format_key(self, key):
        if len(key) == 0:
            raise RuntimeError('key(1,16)长度不能为0')
        #key = list(key), 只能取到一个，实际是2个字节一组
        array = []
        if len(key)<16: # 补位暂时不管
            for i in range(len(key),16):
                key.append(32)
        for i in range(0,32,8):
            array.append(self.convert_bytes2int(key,i))
        return array
    def convert_bytes2int(self,v,offset):
        if offset + 8 >len(v):
            return 0
        num = 0
        for i in range(4):
            hex_bytes = v[offset+i*2:offset+i*2+2]
            #print("type:",type(hex_bytes))
            num = num | self.hex_to_int(hex_bytes) << (8*(3-i))
        return num
    def convert_int2bytes(self, num):
        bs = b''
        for i in range(4):
            int_num = num >> (8*(3-i)) & 255
            bs += self.int_to_hex(int_num)
        return bs
    def hex_to_int(self, hex_bytes):
        #print("type:",type(hex_bytes),hex_bytes)
        b = hex_bytes.decode('utf-8')
        #print(hex_bytes,"<-num->", int('0x'+b,16))
        return int('0x'+b,16)
    def int_to_hex(self, int_num):
        if int_num < 16:
            return b'0' + hex(int_num)[2:].encode('utf-8')
        return hex(int_num)[2:].encode('utf-8')
    def encrypt(self, inner, key = b'B3E2EAABC49B6D9F6FDBC4CFB8E55839',randing=None):
        #inner = inner.decode('utf-8').lower().encode('utf-8')
        #key = key.decode('utf-8').lower().encode('utf-8')
        array2 = b''
        array,num = self.filling(inner,randing)
        for k in range(0,num,8):
            array,array2 = self.code(array,0,k,array2,0,k,key) # *2 是因为python中bytes长度长一倍
        return array2
    def filling(self, inner, randing=None):
        inLen = int(len(inner)/2)
        # 计算头部填充字节数
        num = (inLen + 0x0a) % 8
        if num != 0:
            num = 8 - num
        # 计算输出的密文长度 inLen + num + 10
        rand1 = random.randint(0,255)
        if randing != None:
            rand1 = 1
        array = b'' + bytes([( rand1 & 0xF8) | num]).hex().encode('utf-8') # random.randint(0,255) 1
        # 这里用随机产生的数填充
        for i in range(1, num+3):
            rand1 = random.randint(0,255)
            if randing !=None:
                rand1 = 1
            array = array + bytes([rand1 & 0xFF]).hex().encode('utf-8') #random.randint(0,255) 1学习的时候定位1
        array = array + inner # 加入明文
        # 修改明文 num+3+inlen 到数组长度为0 并补位00
        for j in range(num+3+inLen,num + inLen +10):
            array = array + b'00' # 32
        return array,inLen + num + 10
    def decrypt(self ,inner ,key = b'B3E2EAABC49B6D9F6FDBC4CFB8E55839'):
        #inner = inner.decode('utf-8').lower().encode('utf-8')
        #key = key.decode('utf-8').lower().encode('utf-8')
        inLen = int(len(inner)/2)
        tail = True
        array = b''
        for i in range(inLen):
            pos = (inLen - 1 -i)*2
            if tail:
                if inner[pos: pos+2] == b'03':
                    tail = False
                elif inner[pos: pos+2] == b'00':
                    pass
                else:
                    array = inner[pos: pos+2] + array
                    tail = False
            else:
                array = inner[pos: pos+2] + array
        if inLen%8 !=0 or inLen<16:
            raise RuntimeError('长度不能小于16')
        array2 = b''
        for i in range(0,inLen,8):
            array,array2 = self.decode(array,0,i,array2,0,i,key)
        array2_center = b''
        for i in range(8,inLen):
            a1 = self.hex_to_int(array2[i*2:i*2+2])
            a2 = self.hex_to_int(array[(i-8)*2:(i-8)*2+2])
            array2_center += self.int_to_hex(a1^a2)
        array2_content = array2[0:16] + array2_center
        num = self.hex_to_int(array2_content[0:2])&7
        # num = 8 - num
        inLen = (inLen - num -10)*2
        # print("num:",num,"tes origin:",array2_content[0: num*2+6+inLen])
        return array2_content[num*2+6: num*2+6+inLen]
    def t(self,val):
        val = list(val)
        val[1] = 2
if __name__ == "__main__":
    tea = Tea()
    inner  = b'0018001600010000045300000001000015857DB8666C000000000309000800013D97B49D0001003600120002000100000001000000000000000000000114001D01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA'   
    #inner2 = b'00180012000100000453000000017DB8666C00000000030900800013D97B4A60001003600120002000100000001000000000000000000000114001d01020019027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA'
    key = b'C7FD4ECA0E0D8B2829B5C90CD50DEDB5'
    print(inner,len(inner))
    encrypt_result = tea.encrypt(inner,key)
    print(encrypt_result)
    decrypt_result = tea.decrypt(encrypt_result,key)
    print(decrypt_result)
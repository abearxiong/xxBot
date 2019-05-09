# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:29:42 2019

@author: xiong
"""
import hashlib
import random
import socket
# 所有的看起来hex类型是用来查看，而所有的b类型是用来操作
# 所以得到的hex，需要先执行hex_bytes_2_bytes() 再hex()可以得到 想要的值
class Tool:
    def __init__(self):
        self.name = "Tool"
    def md51(self,pwd):
        md = hashlib.md5()
        md.update(pwd) # 返回byte[]
        hex_str = md.hexdigest()
        bytes_str = hex_str.decode('utf-8')
        return bytes.fromhex(bytes_str)
    def md5(self,user,pwd):
        md = hashlib.md5()
        md.update(pwd) 
        m1 = md.hexdigest() # 第一次hash
        merge = bytes(m1,'utf-8') + bytes('{:016x}'.format(user),'utf-8') # 合并 得到的是16进制的 bytes形式；需要的是hex(bytes) = 其中的内容
        md2 = hashlib.md5() 
        md2.update(bytes.fromhex(merge.decode('utf-8'))) # 得到字符串再生成bytes
        return md2.hexdigest()
    def get_host_by_name(self,ip):
        host = socket.gethostbyname(ip)
        return host
    def get_udp_socket(host,port = 8000):
        st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return st
    def get_random_key(self):
        bytes_hex_all = '0123456789abcdef'
        bytes_random = b''
        for i in range(32):
            j = random.randint(0,15)
            bytes_random = bytes_random + bytes(bytes_hex_all[j],'utf-8')
        return bytes_random
    def hex_bytes_2_bytes(self, hex_bytes):
        return bytes.fromhex(hex_bytes.decode('utf-8'))
    def hex_bytes_2_show_int(self, hex_bytes):
        b = hex_bytes.decode('utf-8')
        return int('0x'+b,16)
    def tea(self):
        print("hh")
    @staticmethod #@classmethod
    def hex_to_int(hex_bytes):
        #print("type:",type(hex_bytes),hex_bytes)
        b = hex_bytes.decode('utf-8')
        #print(hex_bytes,"<-num->", int('0x'+b,16))
        return int('0x'+b,16)
    @staticmethod #
    def int_to_hex(int_num):
        if int_num < 16:
            return b'0' + hex(int_num)[2:].encode('utf-8')
        return hex(int_num)[2:].encode('utf-8')
    @staticmethod
    def hexs_to_int(hex_bytes):
        b = b''
        for i in range(0,len(hex_bytes),2):
            v1 = hex_bytes[i:i+2].decode("utf-8")
            b+= bytes([int("0x"+v1,16)])
        return b
    @staticmethod
    def ints_to_hexs(int_bytes):
        b = b''
        for i in range(0,len(int_bytes)):
            v1 = int_bytes[i]
            if int(v1) <= 0xf:
                hex_str = "0" + hex(v1)[2:]
                b+= hex_str.encode("utf-8")
            else:
                hex_str =  hex(v1)[2:]
                b+= hex_str.encode("utf-8")
        return b
if __name__ =="__main__":
    tool = Tool()
    usr = 2109236844
    pwd = b"123456xx"
    t = tool.md5(usr, pwd)
    print(tool.get_random_key())
    d = b'00010000045300000001000015857DB8666C00000000'
    print(len(d))
    bytes_1 = tool.hex_bytes_2_bytes(b'65')
    print(bytes_1.hex())
    b2 = tool.hex_bytes_2_show_int(b'3d')
    print(b2)
    data = b'\x027\t\x08%65}\xb8fl\x00\x00\x00 \xb9\xa1U\xfa\x0b\xb2\x92`8\xe5\xd1M\xcav$\xe3\x82\x86\xb4f<\xa6j\xa4\xbe\x9e\xc5\x1dEv\xa6\x0c\xd8\x9f\x0b23\xccH\xdc\xdd\x1d\xb8\xd1\xe7\x92Zw\xd9\xee\n\xa2ah\xb0rq\x93@=\xaa\xf6\x94S\xfb\x82\x10\xafL!\x82\xbe\xb6\xf7 O\x815\x8e~z\xbd:\x13\xbd\x1a\xca+\xe4\x86\xe00\x02\xed=\xaa\xcd\xb2\x82\x88\xa7\xdc$v\xcc\xc4\xd7`u\xa8f\xefg\xc6\xb5\xdf\xa05\xc2\x03'
    data = b'\x027\t\x08%65}\xb8fl\x00\x00\x00\xc0\x92\xe77\xe7\x03\x81\xb6pr\xa2\x9f\xf0\xfe\x9a\x16\xb3z\x05\xefn\x9f\xf86\x12w\xb1\xb3\xaa\x9f\x94\x18\x0f\xb8!\xce\xda\x80\xb3\xa7t\xfe\\}KX\xac\xc4\xbb\xe4\xcb\x9e^\xe2\xb7{\xc3Z\x97I\x8b\x94\xd8x\xef]Sg\xaf\r\xc3\x06s\r{\xc5\xccveK\xbb\xfa\x93\xc5B2\xad\xa0\x8cb\x9a\x80M\x12\x92Z&\x17\xd2\xb1@.\xa6X\xdf\xfe\x12<\xf1=\xb7\xa4\x1dI\xe7\r#\xack\xf8\x03'
    b3 = Tool.ints_to_hexs(data)
    print("data",data," length:",len(data),"回应消息",b3)
    
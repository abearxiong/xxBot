# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:45:03 2019

@author: xiong
"""
import socket
from tool import Tool
from tea import Tea
import threading
class Command:
    def __init__(self):
        self.name = "Command"
        self.seq = 0x3635 # (char)Util.Random.Next()
	    #self.end=b'03' #(char)Util.Random.Next()
    def get_0825(self, user):
        pass
class TXProtocol:
    def __init__(self):
        self.CMainVer = b'37' #  0x37 SSO主版本号
        self.CSubVer = b'09' # 0x09 SSO次版本号
        self.Command = b'0825' # 命令 0825 是登录  需要设置
        self.Sequence = b'3635' # Sequence start= 0x3635 为了兼容iQQ iQQ把序列号的高位都为0，如果为1，它可能会拒绝，wqfox称是因为TX是这样做的
        self.QQ = b'7DB8666C'  # QQ  需要设置
        # SendPACKET_FIX
        self.XxooA = b'030000' # Array {0x03, 0x00, 0x00};
        self.DwClientType = b'00010101' #  客户端类型 {0x00, 0x01, 0x01, 0x01};
        self.DwPubNo = b'0000681C' # 发行版本号 {0x00, 0x00, 0x68, 0x1C};
        self.XxooD = b'30000000' # Array {0x03, 0x00, 0x00};
        # Secretkey 加密密钥
        self.SecretKey = b'BDD1F081A82D80EE4E2E89EC85EFC6DA' # 0825key(随机生成16对) 或者其他密钥
        ## 以下加密
        # tlv 0018
        self.tlv0018 = b'0018'
        self.tlv0018DataLength = b'0016' # 下面的数据的长度 len(data)/2 转16进制
        self.wSubVer_tlv0018 = b'0001' # 0x0001 tlv版本 4个
        self.DwSsoVersion = b'00000453' # 0x00000453  主版本号 8个
        self.DwServiceId = b'00000001' # 0x00000001  8个
        self.DwClientVer = b'00001585' # 0x00001585 客户端版本号 
        self.QQtlv = b'7DB8666C' # (uint) user.QQ); //dwUin b'7DB8666C' 8个
        self.WRedirectCount = b'0000' # wRedirectCount 重定向次数 ushort 需要设置;  4个
        self.NullBuf = b'0000' # (ushort) 0); //NullBuf 4个
        
        # tlv 0309
        self.tlv0309 = b'0309'
        self.tlv0309DataLength = b'0008' # 下面的数据的长度 len(data)/2 转16进制
        self.wSubVer_tlv0309 = b'0001' # 0x0001 tlv版本 2个
        self.DwServerIP = b'3D97B4A6' # DwServerIP 4个 { get; set; } = "61.151.226.190";"61.151.180.169"(0x3d,0x97,0xb4,0xa6)61 151 180 166 LastServerIP - 服务器最后的登录IP，可以为0
        self.RedirectIPCount = b'00'  # RedirectIP 的数量 1个
        self.RedirectIP = b'' # RedirectIP 
        self.cPingType = b'01' # 0x01 1个
        
        # tlv 0036
        self.tlv0036 = b'0036'
        self.tlv0036DataLength = b'0012' # 下面的数据的长度 len(data)/2 转16进制
        self.wSubVer_tlv0036 = b'0002' # b'0001' b'0002' 2个
        self.sortWrite = b'00010000000100000000000000000000' #16对 '0001'3对 000100000000 
        
        # tlv 0114
        self.tlv0114 = b'0114'
        self.tvl0114DataLength = b'001D' # 下面的数据的长度 len(data)/2 转16进制
        self.wSubVer_tlv0114 = b'0102' # 0x0114 tlv版本 2个
        self.BufDhPublicKeyLength = b'0019' #  BufDhPublicKey {0x02, 0x78, 0x28, 0x16, 0x7C, 0x9E, 0xF3, 0xB7, 0x5A, 0x7B, 0x5A, 0xEF, 0xA2, 0x30, 0x10, 0xEC, 0x0C, 0x46, 0x87, 0x70, 0x76, 0x31, 0xA7, 0x88, 0xEA};
        self.BufDhPublicKey = b'027828167C9EF3B75A7B5AEFA23010EC0C4687707631A788EA' # 25 对
    def set_value(self,key,value=b''):
        if hasattr(self,key):
            #v = getattr(self,key,None)
            setattr(self, key, value)
        else:
            print('no',key)
            raise RuntimeError('不能没有key')
    def set_login_tlv_length(self,inner):
        inLen = int(len(inner)/2)
        if inLen <= 15:
            v ="000" + hex(inLen)[2:]
            return v.encode("utf-8")
        if inLen <= 255:
            v ="00" + hex(inLen)[2:]
            return v.encode("utf-8")
        return hex(inLen)[2:].encode("utf-8")
    def fill_login_head(self):
        return (b'02' + self.CMainVer + self.CSubVer + self.Command + self.Sequence + self.QQ
                + self.XxooA + self.DwClientType + self.DwPubNo + self.XxooD + self.SecretKey)
    def fill_login_encrypt(self):
        tlv = b''
        tlv0018_content = (self.wSubVer_tlv0018 + self.DwSsoVersion + self.DwServiceId
                          + self.DwClientVer + self.QQtlv + self.WRedirectCount + self.NullBuf)
        #print("length", self.set_login_tlv_length(tlv0018_content))
        tlv0018_content = self.tlv0018 + self.set_login_tlv_length(tlv0018_content) + tlv0018_content
        
        tlv0309_content = (self.wSubVer_tlv0309 + self.DwServerIP +  self.RedirectIPCount
                           + self.RedirectIP + self.cPingType )
        tlv0309_content = self.tlv0309 + self.set_login_tlv_length(tlv0309_content) + tlv0309_content
        
        tlv0036_content = self.wSubVer_tlv0036 + self.sortWrite
        tlv0036_content = self.tlv0036 + self.set_login_tlv_length(tlv0036_content) + tlv0036_content
        
        tlv0114_content = self.wSubVer_tlv0114 + self.set_login_tlv_length(self.BufDhPublicKey) + self.BufDhPublicKey
        tlv0114_content = self.tlv0114 + self.set_login_tlv_length(tlv0114_content) + tlv0114_content
        tlv = tlv + tlv0018_content + tlv0309_content + tlv0036_content + tlv0114_content
        tea = Tea()
        result = tea.encrypt(tlv,self.SecretKey)
        print("加密内容",tlv, " key", self.SecretKey)
        #print("加密结果",result)
        #print("解密",tea.decrypt(result, self.SecretKey))
        return result
    def fill_login_end(self):
        # 如果tcp是要有操作的
        return b'03'
class User:
    def __init__(self, md1 = "", md2 = ""):
        self.md51 = md1
        self.md52 = md2
        self.QQPacket0825Key = b''

class Login:
    def __init__(self,user = 1,pwd=b'123', host = "61.151.180.166", port = 8000):
        host = "61.151.180.158"
        self.tool = Tool()
        self.md2 = self.tool.md5(user,pwd)
        self.user = User(self.md2)
        self.host = self.tool.get_host_by_name(host)
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendPacket = b''
        self.address = (host, port)
        print(self.address)
    def get_md2(self):
        return self.md2
    def set_value(self,key,value=b''):
        if hasattr(self,key):
            #v = getattr(self,key,None)
            setattr(self, key, value)
        else:
            print('no',key)
    def start_fill(self,key=None):
        pro = TXProtocol()
        sp = b'' # sendPacket
        if key != None:
            if type(key) != bytes:
                raise RuntimeError('key must bytes')
            pro.set_value("SecretKey", key)
        #pro.set("", )
        sp += pro.fill_login_head()
        sp += pro.fill_login_encrypt()
        sp += pro.fill_login_end()
        self.sendPacket = sp
        return sp
    def send_0825(self):
        self.start_fill()
        print("发送包",self.sendPacket)
        try:
            pack = Tool.hexs_to_int(self.sendPacket)
            # print(pack)
            #self.udp_socket.sendto(pack,self.address)
            #one_thr = threading.Thread(target = self.get_0825)
            #one_thr.start()
            data = self.udp_socket.recv(2048)
            print("data",data)
        except BaseException:
            print("Error")
    def get_0825(self):
        print("get_0825")
        while True:
            print("get_0825_2048_START")
            data = self.udp_socket.recv(2048)
            print(data)
            print("get_0825_2048_END")
def sendFun():
    print("method sendFun()")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = "61.151.180.158" # 61.151.180.166
    address = (host,8000)
    val = b'023709082536367DB8666C030000000101010000681C30000000752406735B804AF4861322F9A09E938E5AC2CD0E0A7C9018AA16B16400AA6253BED51F86A2C6DDB1C7E85B5444DDA02B57DB7E324EF798584CE703BFB8FCC5A0F6586A5CF2D6DCF6151B2EC16CB7311EB9EE87D24D32217B7779E9BB0184D4B2ADC8B0BEA6CE776629ED8AEBDE8B3DDA4BACE8AFEB2E6CC803'
    print(s)
    #s.sendto(val, address)
    #data = s.recv(2048)
    #print(data)
if __name__ =="__main__":
    login = Login(2109236844,b"123456xx")
    md2 = login.get_md2()
    login.send_0825()
    #sendFun()
    #print(md2)
    #print(vars(login))
    
def send_and_get():
    skey = b'BDD1F081A82D80EE4E2E89EC85EFC6DA'
    sendP = b'023709082536357DB8666C030000000101010000681C30000000BDD1F081A82D80EE4E2E89EC85EFC6DABE32EBD9156C69E1DD9FC2A8D562707F7ED45130EF51B66560DC197C8B90037796478D1005F43896514A33EF399589EED184C4CDFEEF3F1BEB4CFB31A20FF408F9824BCC55B67D6044390B1EE23CDD817950B63471EE0F30359BDD4105DAD7C73559AF3D20404B3203'
    getP =  b'023709082536357db8666c000000c092e737e70381b67072a29ff0fe9a16b37a05ef6e9ff8361277b1b3aa9f94180fb821ceda80b3a774fe5c7d4b58acc4bbe4cb9e5ee2b77bc35a97498b94d878ef5d5367af0dc306730d7bc5cc76654bbbfa93c54232ada08c629a804d12925a2617d2b1402ea658dffe123cf13db7a41d49e70d23ac6bf803'
    print("SEND",sendP,"GET",getP)
    gParse =b'c092e737e70381b67072a29ff0fe9a16b37a05ef6e9ff8361277b1b3aa9f94180fb821ceda80b3a774fe5c7d4b58acc4bbe4cb9e5ee2b77bc35a97498b94d878ef5d5367af0dc306730d7bc5cc76654bbbfa93c54232ada08c629a804d12925a2617d2b1402ea658dffe123cf13db7a41d49e70d23ac6bf8'
    gParse =b'A20A7EBE3787E02D11456A4EA0F2C22C61ABD68617C1C98F93AF645D702F3DDC74AC47A6B9F8E5A1F85040613F037795DEBC92C0A05D453CC34C4385384A53707DA8926F5FB47A5F95D70D40E743DC303916FA46229E1CC261C409CF71E6B72841C83261B324E386'
    tea = Tea()
    v = tea.decrypt(gParse,skey)
    print("v",v)
    # 明文
    body_1 = b'0001120038372E3F12229301ED7089964781B0AC0ECCDB34DD00E2992BE67482C08173B49AC5371A7B93348965C41B4D69C7900BDDDD2255E89074FA2B0017000E00015CD3BD23B6964C1DCECE0000031000043D97B49E'
    # 密钥
    skey_1 = b'59C7E081E5F824D73C5E1009FA114A9A'
    # 生成解密
    encrypt_1 = tea.encrypt(body_1,skey_1)
    # 原始加密内容 -- 随机数不同 加密内容是不同的
    encrypt_1_2 = b'91FF3B36AD54BB1ED562AC532E1A31F970DE95BA4162C3672853E2F763AF997A3AE0494A1E45F4F77C1C3417D19307B190659946601692C7A6F6C20618ABA35DEC597B57C4AAAF98208D96855476428A93916D8C212FAEF99A72236C52EB6BCA6472FCD4E73A37CE'
    #print(encrypt_1, encrypt_1_2)
    result_1 = tea.decrypt(encrypt_1,skey_1)
    print("r1",result_1)
    result_1_2 = tea.decrypt(encrypt_1_2,skey_1)
    print("r2",result_1_2)
    print(body_1)
    # 明文
    body_2 = '0001120038372E3F12229301ED7089964781B0AC0ECCDB34DD00E2992BE67482C08173B49AC5371A7B93348965C41B4D69C7900BDDDD2255E89074FA2B0017000E00015CD3BD23B6964C1DCECE0000031000043D97B49E'
    # 密钥
    skey_2 = '59C7E081E5F824D73C5E1009FA114A9A'
    # 生成解密
    encrypt_2 = tea.encrypt(body_2.lower().encode("utf-8"),skey_2.lower().encode("utf-8"))
    decrypt_2 = tea.decrypt(encrypt_2, skey_2.lower().encode("utf-8"))
    print(encrypt_2,decrypt_2)
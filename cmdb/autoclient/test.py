import time
import uuid
import requests
import hashlib

# ctime = time.time()
# key = "asdfasdfasdfasdf098712sdfs"
# new_key = "%s|%s" %(key,ctime)
#
# m = hashlib.md5()
# m.update(bytes(new_key,encoding='utf-8'))
# md5_key = m.hexdigest()
#
# md5_time_key = "%s|%s" %(md5_key,ctime)
# print(md5_time_key)
#
# # response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':key})
# response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':md5_time_key})
# # response = requests.get("http://127.0.0.1:8000/api/asset.html")
# print(response.text)


from Crypto.Cipher import AES

# key = b'fgthjgjuytrfdvcb'
# cipher = AES.new(key,AES.MODE_CBC,key)
# msg = cipher.encrypt()


# data = "要加密的字符串...."
# ba_data = bytearray(data,encoding='utf-8')
# v1 = len(ba_data)
# v2 = v1 % 16
# if v2 == 0:
#     v3 = 16
# else:
#     v3 = 16 - v2
# for i in range(v3):
#     ba_data.append(v3)
# print(ba_data)
# final_data = ba_data.decode('utf-8')
# print(final_data)

# #########################解密############################
# miwen = b'dfdfdddddddddddddsdfdfdfdfsdffffffffdfdfdfdf'
# key = b'fgthjgjuytrfdvcb'
# cipher = AES.new(key.MODE_CBC,key)
# result = cipher.decrypt(miwen)
# data = result[0:-result[-1]]


# result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe7\x9a\x84\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2....\x07\x07\x07\x07\x07\x07\x07'
# print('最后一个字节：',result[-1])
# data = result[0:-result[-1]]
# print(data)
# print(str(data,encoding='utf-8'))


import json
import requests
from Crypto.Cipher import AES
def encrypt(message):
    """
    加密
    :param message:
    :return:
    """
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    ba_data = bytearray(message,encoding='utf-8')
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):
        ba_data.append(v3)
    final_data = ba_data.decode('utf-8')
    msg = cipher.encrypt(final_data) # 要加密的字符串，必须是16个字节或16个字节的倍数
    return msg

# ############################## 解密 ##############################
def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')


def auth():
    import time
    import requests
    import hashlib

    ctime = time.time()
    key = "asdfasdfasdfasdf098712sdfs"
    new_key = "%s|%s" %(key,ctime,)

    m = hashlib.md5()
    m.update(bytes(new_key,encoding='utf-8'))  #里面是字节数据
    md5_key = m.hexdigest()                    #返回值是字符窜类型

    md5_time_key = "%s|%s" %(md5_key,ctime)

    return md5_time_key

# response = requests.post(url="http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':auth()},json={'k1':'v1'})
# v1 = bytes(json.dumps({'k1':'v1'}),encoding='utf-8')

v1 = encrypt(json.dumps({'k1':'v1','k2':'v2asdfasdfasdfasdfasdfasdfasdf'}))
print(v1)
response = requests.post(
    url="http://127.0.0.1:8000/api/asset.html",
    headers={'OpenKey':auth(),'Content-Type':'application/json'},
    data=v1
)
print(response.text)

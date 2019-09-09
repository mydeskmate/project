__author__ = 'Administrator'

# #################### Agent,每一台服务器一份 ####################
# import subprocess
# v1 = subprocess.getoutput('ipconfig')
# # 模拟正则或其他方式获取需要的数据
# value1 = v1[20:30]
#
# v2 = subprocess.getoutput('dir')
# value2 = v2[0:5]
#
# # 连接数据库，写到数据库
#
# url = "http://127.0.0.1:8000/asset.html"
# import requests
#
# response = requests.post(url,data={'k1':value1,'k2':value2})
# print(response.text)

# #################### Paramiko,中控机放一份 ####################
"""
- 远程连接服务器，执行命令，获取结果
- 将结果发送API
192.168.11.98
"""

import paramiko

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='172.16.1.101', port=22, username='root', password='tfedu6188')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('ls')
# 获取命令结果
result = stdout.read()

# 关闭连接
ssh.close()

value = result[0:10]
print(value)

url = "http://127.0.0.1:8000/asset.html"
import requests

response = requests.post(url,data={'k1':value,'k2':value})
print(response.text)










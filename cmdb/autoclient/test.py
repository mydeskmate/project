import time
import uuid
import requests
import hashlib

ctime = time.time()
key = "asdfasdfasdfasdf098712sdfs"
new_key = "%s|%s" %(key,ctime)

m = hashlib.md5()
m.update(bytes(new_key,encoding='utf-8'))
md5_key = m.hexdigest()

md5_time_key = "%s|%s" %(md5_key,ctime)
print(md5_time_key)

# response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':key})
response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':md5_time_key})
# response = requests.get("http://127.0.0.1:8000/api/asset.html")
print(response.text)
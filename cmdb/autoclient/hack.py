__author__ = 'Administrator'

import requests

response = requests.get(url='http://127.0.0.1:8000/api/asset.html',headers={"OpenKey":"cc55b2e0564917b8a27d3a178c7716f8|1568687589.937025"})
print(response.text)
import requests
import json
from src.plugins import PluginManager
from lib.conf.config import settings
from concurrent.futures import ThreadPoolExecutor

class Base(object):
    """
    基类，方法重用
    """
    def post_asset(self,server_info):
        """
        向API发送资产信息
        :param server_info:
        :return:
        """
        r = requests.post(settings.API,json=server_info)
        print(r.text)

class Agent(Base):
    """
    Agent类
    """
    def execute(self):
        server_info = PluginManager().exec_plugin()
        hostname = server_info['basic']['data']['hostname']
        certname = open(settings.CERT_PATH,'r',encoding="utf-8").read().strip()
        if not certname:
            with open(settings.CERT_PATH,'w',encoding="utf-8") as f:
                f.write(hostname)
        else:
            server_info['basic']['data']['hostname'] = certname
        self.post_asset(server_info)


class SSHSALT(Base):
    """
    ssh或salt类
    """
    def get_host(self):
        """
        获取未采集的主机列表：
        :return:
        """
        response = requests.get(settings.API)
        result = json.loads(response.text)
        if not result['status']:
            return
        return result['data']

    def run(self,host):
        server_info = PluginManager(host).exec_plugin()
        self.post_asset(server_info)


    def execute(self):
        host_list = self.get_host()
        pool = ThreadPoolExecutor(10)
        for host in host_list:
            pool.submit(self.run,host)

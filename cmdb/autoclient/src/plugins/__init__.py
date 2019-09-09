import importlib
import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

from lib.conf.config import settings

class PluginManager(object):
    def __init__(self,hostname=None):
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT

        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD


    def exec_plugin(self):
        """
        获取所有的插件，并执行获取插件返回值
        :return:
        """
        response = {}
        for k,v in self.plugin_dict.items():
            module_path,class_name = v.rsplit('.',1)
            m = importlib.import_module(module_path)
            cls = getattr(m,class_name)
            if hasattr(cls,'initial'):
                obj = cls.initial()
            else:
                obj = cls()
            result = obj.process(self.command,self.debug)
            response[k] = result
        return response

    def command(self,cmd):
        """
        执行系统命令
        :param cmd:
        :return:
        """
        if self.mode == "AGENT":
            return self.__agent(cmd)
        elif self.mode == "SSH":
            return self.__ssh(cmd)
        elif self.mode == "SALT":
            return self.__salt(cmd)
        else:
            raise Exception('模式只能是AGENT/SSH/SALT')

    def __agent(self,cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self,cmd):
        salt_cmd = "salt '%s' cmd.run '%s'" % (self.hostname,cmd,)
        import subprocess
        output = subprocess.getoutput(salt_cmd)
        return output

    def __ssh(self,cmd):
        import paramiko

        # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # result = stdout.read()
        # ssh.close()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user,passphrase=self.ssh_pwd)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        result = stdout.read()
        ssh.close()
        return result
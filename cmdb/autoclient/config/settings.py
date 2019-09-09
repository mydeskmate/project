"""
用户自定义配置文件
"""


USER = 'root'
PWD = '123456'

SSH_USER = "root"
SSH_PWD = "tfedu6188"
SSH_KEY = "/xxx/xxx/xx"
SSH_PORT = 22

MODE = "AGENT"    #SALT, SSH
DEBUG = True


PLUGINS_DICT = {
    'basic': "src.plugins.basic.Basic",
    'board': "src.plugins.board.Board",
    'cpu': "src.plugins.cpu.Cpu",
    'disk': "src.plugins.disk.Disk",
    'memory': "src.plugins.memory.Memory",
    'nic': "src.plugins.nic.Nic",
}
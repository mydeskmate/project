import os
os.environ['USER_SETTINGS'] = "config.settings"
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)




if __name__ == '__main__':
    from src.plugins import PluginManager
    server_info = PluginManager().exec_plugin()
    print(server_info)

import time
import sys,os
import multiprocessing




if __name__ == "__main__":
    # 配置django 环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HanAudit.settings")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE_DIR)
    print(sys.path)
    import django
    django.setup()
    from audit import models

    task_id = sys.argv[1]

    #1. 根据Taskid拿到任务对象，
    #2. 拿到任务关联的所有主机
    #3.  根据任务类型调用多进程 执行不同的方法
    #4 . 每个子任务执行完毕后，自己八结果写入数据库






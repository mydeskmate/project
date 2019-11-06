
import json
from audit import models
import subprocess
from django.conf import settings
from django.db.transaction import atomic

class Task(object):
    """处理批量任务，包括命令和文件传输"""
    def __init__(self,request):
        self.request = request
        self.errors = []
        self.task_data = None

    def is_valid(self):
        """
        1. 验证命令、主机列表合法
        :return:
        """
        task_data = self.request.POST.get('task_data')
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get('task_type') == 'cmd':
                if self.task_data.get('cmd') and self.task_data.get('selected_host_ids'):
                    return True
                elif self.task_data.get('cmd') and self.task_data.get('dest') == 'stop':
                    return True
                self.errors.append({'invalid_argument': 'cmd or host_list is empty.'})
            elif self.task_data.get('task_type') == 'file_transfer':
                return True #self.errors.append({'invalid_argument':'cmd or host_list is empty.'})
            else:
                self.errors.append({'invalid_argument':'task_type is invalid.'})
        self.errors.append({'invalid_data':'task_data is not exist '})


    def run(self):
        """start task , and return task id """
        task_func = getattr(self, self.task_data.get('task_type'))
        task_dest = self.task_data.get('dest')
        if task_dest:
            task_obj = task_func(task_dest)
        task_obj = task_func()
        return task_obj

    @atomic
    def cmd(self,*args):
        """批量任务"""
        #print("run multi task.....")
        print(args)
        selected_host_ids = []
        if args == 'stop':
            stop_task_id = self.task_data.get('task_id')
            stop_task_obj = models.Task.objects.filter(id=stop_task_id).first()
            for host_user in  stop_task_obj.tasklog_set.host_user_bind:
                selected_host_ids.append(selected_host_ids.host_id)
            print(selected_host_ids)

        task_obj = models.Task.objects.create(
            task_type = 0,
            account = self.request.user.account ,
            content = self.task_data.get('cmd'),
            #host_user_binds =
        )

        selected_host_ids = self.task_data.get("selected_host_ids")
        tasklog_objs = []
        host_ids = set(selected_host_ids)
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status = 3
                               )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs,100)
        #task_obj.host_user_binds.add(1,2,3)
        #task_obj.host_user_binds.add(*self.task_data.get('selected_host_ids'))

        #执行任务

        # for host_id in self.task_data.get('selected_host_ids'):
        #     t = Thread(target=self.run_cmd,args=(host_id,self.task_data.get('cmd')))
        #     t.start()
        #
        # cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT,task_obj.id)   该命令再linux执行出错
        cmd_str = ["python", settings.MULTI_TASK_SCRIPT, str(task_obj.id)]
        pid = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE )
        # print("task result :",multitask_obj.stdout.read(),multitask_obj.stderr.read().decode('gbk'))
        # print(cmd_str)
        # tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)

        return  task_obj

    def file_transfer(self):
        """批量文件"""

        task_obj = models.Task.objects.create(
            task_type = 1,
            account = self.request.user.account ,
            content = json.dumps(self.task_data),
            #host_user_binds =
        )
        tasklog_objs = []
        host_ids = set(self.task_data.get("selected_host_ids"))
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status = 3
                               )
            )
        models.TaskLog.objects.bulk_create(tasklog_objs,100)

        # cmd_str = "python %s %s" % (settings.MULTI_TASK_SCRIPT,task_obj.id)
        cmd_str = ["python", settings.MULTI_TASK_SCRIPT, str(task_obj.id)]
        multitask_obj = subprocess.Popen(cmd_str,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE )
        # print("task result :",multitask_obj.stdout.read(),multitask_obj.stderr.read().decode('gbk'))
        # print(cmd_str)
        return  task_obj
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
class M1(MiddlewareMixin):

    def process_request(self,request,*args,**kwargs):
        pass
        ## 进行后面的测试，先取消权限验证
        valid = ['/auth_index.html','/auth_login/']

        if request.path_info not in valid:
            print(request.path_info)
            action = request.GET.get('md').upper() # GET
            user_permission_dict = request.session.get('user_permission_dict')
            if not user_permission_dict:
                return HttpResponse('无权限')

            print(user_permission_dict)
            #正则匹配
            # action_list = user_permission_dict.get(request.path_info)
            flag = False
            for k,v in user_permission_dict.items():
                if re.match(k,request.path_info):
                    if action in v:
                        flag = True
                        break
            if not flag:
                return HttpResponse('无权限')

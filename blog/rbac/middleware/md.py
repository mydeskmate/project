from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from rbac import config
import re
class RbacMiddleware(MiddlewareMixin):

    def process_request(self,request,*args,**kwargs):
        # pass
        ## 进行后面的测试，先取消权限验证
        # valid = ['/auth_index.html','/auth_login/','/index.html']
        # 预定义放行的url
        for pattern in config.VALID_URL:
            if re.match(pattern,request.path_info):
                return None

        # 后台用户定义的url
        action = request.GET.get('md') # GET
        if action:
            action = action.upper()
        user_permission_dict = request.session.get('user_permission_dict')
        # print(user_permission_dict)
        if not user_permission_dict:
            # print(user_permission_dict)
            return HttpResponse('无权限')

        # print(user_permission_dict)
        #正则匹配
        # action_list = user_permission_dict.get(request.path_info)
        flag = False
        print(user_permission_dict)
        for k,v in user_permission_dict.items():
            if re.match(k,request.path_info):
                # print(v)
                # print(action)
                if action in v:
                    flag = True
                    break
        if not flag:
            return HttpResponse('无权限')

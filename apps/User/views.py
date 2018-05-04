from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from apps.User.models import User
from django_redis import get_redis_connection
from django.core.mail import send_mail
import re
from DailyFresh import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from celery_tasks.tasks import send_register_active_email
import re
import random
from DailyFresh.settings import APIKEY
# from .models import VerifyCode
from utils.yunpian import YunPian


class RegisterView(View):
    """获取手机验证码"""
    def get(self, request):
        return render(request, 'register2.html')

    def post(self,request):
        mobile=request.POST.get('mobile')
        # uuid =request.POST.get('uuid')
        print(mobile)
        # print(uuid)

        if mobile:
            #验证是否为有效手机号
            mobile_pat=re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
            res=re.search(mobile_pat,mobile)

            if res:
                #生成手机验证码
                # code=VerifyCode()
                # code.mobile=mobile
                # c=random.randint(1000,9999)
                # code.code=str(c)
                # code.save()
                # code=VerifyCode.objects.filter(mobile=mobile).first().code
                code = '%06d' % random.randint(0, 999999)   #
                print(code)
                # yunpian=YunPian(APIKEY)  # 调用云片发送短信验证码
                # sms_status=yunpian.send_sms(code=code,mobile=mobile)
                # print(sms_status)
                # print(sms_status)
                # print(sms_status.status_code)
                # print(sms_status.status_code)
                # print(type(sms_status.status_code))
                # sms_status.status_code = 200
                # if sms_status.status_code == 200:
                #     conn = get_redis_connection('default')
                #     conn.set('Mobile:' + mobile, code, 3600)
                #     return JsonResponse({'res': 0})

                status_code = 200
                if status_code == 200:
                    conn = get_redis_connection('default')
                    conn.set('Mobile:' + mobile, code, 3600)
                    return JsonResponse({'res': 0})
            else:
                msg='请输入有效手机号码!'
                return JsonResponse({'msg': msg})
        else:
            msg='手机号不能为空！'
            return JsonResponse({'msg': msg})


class ChangeView(View):
    def post(self,request):
        mobile=request.POST.get('mobile')
        phonecode = request.POST.get('phonecode')
        password =request.POST.get('password')

        print(mobile)
        print('验证码是%s' % phonecode)
        print('密码是%s' % password)
        print(type(phonecode))

        if not all([mobile, phonecode, password]):
            # return render(request, 'register2.html', {'errormsg': '请填写全部参数'})
            return JsonResponse({'errormsg': '请填写全部参数'})
        if len(password)<8:
            # return render(request, 'register2.html', {'errormsg': '密码位数至少为8位'})
            return JsonResponse({'errormsg': '密码位数至少为8位'})
        try:
            conn = get_redis_connection('default')
            phone_code = conn.get('Mobile:' + mobile)

            print(phone_code)
        except Exception as e:
            # return render(request, 'register2.html', {'errormsg': '查询验证码失败'})
            return JsonResponse({'errormsg': '查询验证码失败'})

        if int(phone_code) != int(phonecode):
            print(int(phone_code))

            return JsonResponse({'errormsg': '验证码错误'})

        # user = User.objects.get(username = mobile)
        # print(user)
        # if not user:
        #     user = User.objects.create_user(username=mobile, password=password)
        #     user.save()
        # else:
        #     return JsonResponse({'errormsg': '该手机号码已注册'})
            # return JsonResponse({'errormsg': '该手机号码已注册'})
        try:
            user = User.objects.get(username=mobile)
            print(user)
            return JsonResponse({'errormsg': '该手机号码已注册'})
        except Exception as e:
            user = User.objects.create_user(username=mobile, password=password)
            user.save()
            print(e)

        return JsonResponse({'res': 1})


# Create your views here.
# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'register.html')
#
#     def post(self, request):
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#
#         if not all([username, password, email]):
#             return render(request, 'register.html', {'errormsg': '请填写全部内容'})
#         if len(password) < 8:
#             return render(request, 'register.html', {'errormsg': '密码不能少于8位'})
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errormsg': '邮箱格式错误'})
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#         if user is not None:
#             return render(request, 'register.html', {'errormsg': '用户名已注册'})
#
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#
#         serializer = Serializer(settings.SECRET_KEY, 3600)
#         info = {'confirm': user.id}
#         token = serializer.dumps(info)
#         token = token.decode()
#         # subject = 'DailyFresh'
#         # message = ''
#         # email_from = settings.EMAIL_FROM
#         # receiver = [email]
#         # html_message = """
#         # <h1>%s, 欢迎您成为天天生鲜注册会员</h1>
#         # 请在一小时之内完成注册激活
#         # <a href='http://127.0.0.1:8000/user/active/%s'>http://127.0.0.1:8000/user/active/%s</a>
#         # """ % (username, token, token)
#         # send_mail(subject, message, email_from, receiver, html_message=html_message)
#         send_register_active_email(email, username, token)
#         return redirect(reverse('goods:index'))


# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'register2.html')
#
#     def post(self, request):
#         phone = request.POST.get('phone')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#
#         if not all([phone, password, email]):
#             return render(request, 'register2.html', {'errormsg': '请填写全部内容'})
#         if len(password) < 8:
#             return render(request, 'register2.html', {'errormsg': '密码不能少于8位'})
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register2.html', {'errormsg': '邮箱格式错误'})
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#         if user is not None:
#             return render(request, 'register2.html', {'errormsg': '用户名已注册'})
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         user.save()
#
#         return redirect(reverse('goods:index'))



class ActiveView(View):
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired:
            return HttpResponse('链接已失效')


class LoginView(View):
    def get(self, request):
        username = request.COOKIES.get('username')
        checked = 'checked'
        if username is None:
            username = ''
            checked = ''
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')
        if not all([username, password]):
            return render(request, 'register.html', {'errormsg': '请填写全部内容'})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # 获取用户登录之前访问的url地址，默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))  # None
                response = redirect(next_url)  # HttpResponseRedirect

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, 'login.html', {'errormsg': '用户未激活'})

        else:
            return render(request, 'login.html', {'errormsg': '用户名或者密码错误'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))



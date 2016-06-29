#-*-coding:utf-8-*-
import requests
import json
import re
from hotelBooking.utils import modelKey
from hotelBooking.utils.decorators import parameter_necessary,method_route,is_authenticated
from hotelBooking.utils.AppJsonResponse import JSONWrappedResponse,DefaultJsonResponse
from . import User,CustomerMember
from .serializers import *
from .utils import userhelper
import logging
from . import appcodes

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST

from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save

from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes,permission_classes,authentication_classes,detail_route,list_route
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from qiniu import Auth
from rest_framework_jwt.settings import api_settings


jwt_payload_handle = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

logger = logging.getLogger(__name__)

APP_ID = "P0fN7ArvLMtcgsACRwhOupHj-gzGzoHsz"
APP_KEY = "cWK8NHllNg7N6huHiKA1HeRG"


class AppConst:
    STATUS_SUCCESSS = '100'
    STATUS_ERROR = '-100'
    STATUS_PWD_ERROR = '102'
    STATUS_PHONE_EXISTED = '103'
    STATUS_PHONE_NOT_EXISTED = '104'


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


@parameter_necessary('phoneNumber', )
@never_cache
@require_POST
def member_resiter_sms_send(request):
    phoneNumber = request.POST.get(modelKey.KEY_PHONENUMBER)
    print('regist phone number %s'%phoneNumber)
    smsType = request.POST.get('smsType')
    if (userhelper.phoneNumberExist(phoneNumber)):
        return DefaultJsonResponse(code=appcodes.CODE_PHONE_IS_EXISTED, message="手机号已经存在")
    url = 'https://api.leancloud.cn/1.1/requestSmsCode'
    values = {
        modelKey.KEY_LEAN_PHONENUMBER: str(phoneNumber),
        "template": "register",
    }
    if smsType == '2':
        values['smsType'] = 'voice'
    else:
        pass
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    print(values)
    response = requests.post(url, data=json.dumps(values), headers=headers)
    # 使用异步
    # print(response.status_code)
    # print(str(response.content))
    # print(response.request.body)
    if response.status_code == 200:
        return DefaultJsonResponse(code=appcodes.CODE_100_OK, message='发送验证码成功')
    else:
        response_dic = response.json()
        return DefaultJsonResponse(code=response_dic['code'], message=response_dic['error'])


@never_cache
@api_view(['POST',])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@parser_classes((JSONParser,))
def installationId_register(request, formate=None):
    json = request.data
    print(str(json))
    serializer = InstallationSerializer(data=json)
    if serializer.is_valid():
        print('valid'+serializer.__str__())
        serializer.save()
        return DefaultJsonResponse(code=appcodes .CODE_100_OK, message="上传成功")
    else:
        print(serializer.errors)
        return DefaultJsonResponse(code=AppConst.STATUS_ERROR, message=str(serializer.errors))


access_key = 'u-ryAwaQeBx9BS5t8OMSPs6P1Ewoqiu6-ZbbMNYm'
secret_key = 'hVXFHO8GusQduMqLeYXZx_C5_c7D-VSwz6AKhjZJ'


@api_view(['GET','POST',])
def update_user_avatar_callback(request):
    """
    采用 用户发起请求，获取ｔｏｋｅｎ，客户端得到token往　七牛云上传图片，七牛云回调我方接口的调用流程
    这个接口是  在用户上传之后 ，七牛云回调的我方接口
    :param request:
    :return:
    """
    post_data =  request.POST
    f_name = post_data.get('filename')
    f_size = post_data.get('filesize')
    print(type(re.match('^avatar_(?P<id>\d+).*', f_name)))
    try:
        phone_number = re.match('^avatar_(?P<id>\d+).*',f_name).group('id')
        if(phone_number and User.existPhoneNumber(phone_number= phone_number)):
            userhelper.updateAvatar(phone_number,f_name)
            print('update avatar success')
        else:
            print('update avatar error')
    except BaseException as e:
        print('发生异常了')
        print(e.__traceback__)
    return Response('OK')

# -------------------------基于类的视图----------------------------------------------#

class UserViewSet(UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = CustomerMemberSerializer
    queryset = User.objects.all()


    @method_route(methods=['POST'],)
    @method_decorator(parameter_necessary('phoneNumber', 'password', 'smsCode',))
    def register(self, request):
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        sms_code = request.POST.get('smsCode', None)
        print(sms_code)
        if (not userhelper.phoneNumberExist(phone_number)):
            if sms_code != None:
                # verifySuccess, message = verifySmsCode(phone_number, password)
                if (True):
                    try:
                        member = CustomerMember()
                        print('member 的phoneNumber' + str(member.phone_number))
                        member.phone_number = phone_number
                        member.set_password(password)
                        member.username = phone_number
                        print('member 的username =' + str(member.username))
                        serializer_member = CustomerMemberSerializer(member, many=False)
                        # serializer_member.data
                        kwargs = {'UserEntity': serializer_member.data}
                        payload = jwt_payload_handle(member)
                        token = jwt_encode_handler(payload)
                        member.save()
                    except BaseException as e:
                        # raise e
                        return DefaultJsonResponse(res_data= kwargs, code=appcodes.CODE_NEGATIVE_100_APP_ERROR, message="内部错误")
                    else:
                        response = DefaultJsonResponse(res_data= kwargs, code=appcodes.CODE_100_OK, message="注册成功")
                        response['token'] = token
                        return response
                else:
                    return DefaultJsonResponse(code=appcodes.CODE_SMS_ERROR, message="注册失败，验证码错误")

        else:
            return DefaultJsonResponse(code=appcodes.CODE_PHONE_IS_EXISTED, message="手机号已经存在")

    @method_route(methods=['POST'],)
    @method_decorator(is_authenticated())
    def logout(self,request):
        print(request.user)
        if(isinstance(request.user,AnonymousUser)):
            return Response('都没登入过叫个锤子啊')
        else:
            return DefaultJsonResponse(code=100,message="退出成功")

    @method_route(methods=['PUT'], url_path='password')
    @method_decorator(parameter_necessary('phoneNumber', 'password', ))
    def change_password(self,request):
        phoneNumber = request.POST['phoneNumber']
        password = request.POST['password']

        print('phoneNumber is {0} and password is {1}'.format(phoneNumber,password))
        return DefaultJsonResponse(res_data='修改失败')

    @method_route(methods=['PUT'],url_path='profile')
    @method_decorator(is_authenticated())
    def update_profile(self,request):
        print(request.user)
        s = UpdateCustomerMemberSerializer(data=request.data)
        s.is_valid()
        print(s.errors)
        if(s.is_valid()):
            s.update(request.user,s.validated_data)
            return DefaultJsonResponse(message='修改用户资料成功')
        else:
            return DefaultJsonResponse(message='修改失败{0}'.format(s.errors.values),code='-100')


    @method_route(methods=['POST'], url_path='installation/bind')
    @method_decorator(is_authenticated())
    def bind_installationId(self,request):
        phoneNumber = request.user.pk
        installationId = request.POST.get('installationId')
        deviceToken = request.POST.get('deviceToken')
        if installationId:
            try:
                installDevice = Installation.objects.get(installationId=installationId)
                user = User.objects.get(phone_number=phoneNumber)
                installDevice.member = user
                installDevice.save()
                return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="success")
            except Installation.DoesNotExist:
                return DefaultJsonResponse(code=appcodes.CODE_INSTALLATION_BIND＿FAILED_NOT_UPLOADED, message="这个installationId尚未注册到服务端")
        elif deviceToken:
            return DefaultJsonResponse(code=appcodes.CODE_100_OK, message="ios还没写,哇咔咔")

    @method_route(methods=['GET',],url_path='avatar/token')
    @method_decorator(is_authenticated())
    def avatar_token(self,request):
        q = Auth(access_key, secret_key)
        bucket_name = 'hotelbook'
        phone_number = request.user.phone_number
        imageName = '/avatar/avatar_' + str(phone_number) + '.jpg'
        key = imageName
        policy = {
            'callbackUrl':'agesd.com/avatar/upload/callback',
            'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        }
        token = q.upload_token(bucket_name, key, 3600,policy)
        return DefaultJsonResponse(code=appcodes.CODE_100_OK,
                                   res_data={'upload_token': token, 'imageUrl': key})

class HotelViewSet(viewsets.GenericViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(request.POST)
        print(request.GET)
        print(request.query_params)

        city_id = request.query_params.get('cityId')
        hotels = queryset.all()
        if city_id is not  None:
            hotels =hotels.filter(city_id=city_id).all()
        try:
            page = request.query_params.get('page',1)
            if int(page) < 1 :
                page =1
        except ValueError as e:
            print('catch error'+e.__str__())

        print(hotels)
        paginator = Paginator(hotels,1)
        try:
            backHotels = paginator.page(page)
            serializers = self.serializer_class(backHotels,many=True,excludes=('houses',))
        except EmptyPage as e:
            return DefaultJsonResponse(code=-100, message='没有更多数据')
        return DefaultJsonResponse(res_data={'hotels': serializers.data})


# class HotelListView(ListAPIView):
#     serializer_class = HotelSerializer
#     queryset = Hotel.objects.all()
#
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     print(request.POST)
    #     print(request.GET)
    #     print(request.query_params)
    #     city_id = request.query_params.get('cityId')
    #     hotels =queryset.filter(city_id=city_id)
    #     try:
    #         page = request.query_params.get('page',1)
    #         if int(page) < 1 :
    #             page =1
    #     except ValueError as e:
    #         print('catch error'+e.__str__())
    #
    #     print(hotels)
    #     paginator = Paginator(hotels,1)
    #     try:
    #         backHotels = paginator.page(page)
    #         serializers = self.serializer_class(backHotels,many=True,excludes=('houses',))
    #     except EmptyPage as e:
    #         return DefaultJsonResponse(code=-100, message='没有更多数据')
    #     return DefaultJsonResponse(res_data={'hotels': serializers.data})

class HouseViewSet(viewsets.GenericViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()
    lookup_url_kwarg =  ['fuck',]

    def list (self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        return Response('fuck you')

class ProvinceView(ListAPIView):
    serializer_class = ProvinceSerializer
    queryset= Province.objects.all()

    def get(self, request):
        provinces = Province.objects.all()
        serializer_provinces = ProvinceSerializer(provinces, many=True)
        data = {'procinces': serializer_provinces.data,}
        return DefaultJsonResponse(res_data=data, )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# ----------------------------- NonView Method---------------------------------------
def verifySmsCode(mobilePhoneNumber, smscode):
    url = 'https://api.leancloud.cn/1.1/verifySmsCode/' + str(smscode)
    print(url)
    values = {
        "mobilePhoneNumber": str(mobilePhoneNumber),
    }
    headers = {'X-LC-Id': APP_ID, 'X-LC-Key': APP_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, params=values)
    response.encoding = 'utf-8'
    # 使用异步
    print(response.content)
    print(response.status_code)
    print(type(response.json()))
    if response.status_code == 200:
        return True, "Success"
    elif response.json().get('code', 0) == 603:
        # Invalid SMS code
        print(response.json()['code'])
        return False, "Invalid SMS code"
    else:
        return False, "尚未处理的错误"


def phoneNumberExist(phoneNumber):
    return User.objects.exists(phoneNumber=phoneNumber)


def parse_get_userId(request):
    userId = request.REQUEST.get('userId')
    return userId

from rest_framework.views import exception_handler


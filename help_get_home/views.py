#coding=utf-8
default_encoding='utf-8'
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.template import loader,Context   
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.utils.six import BytesIO
from django.core.paginator import Paginator
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from rest_framework.settings import api_settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token

from help_get_home.serializers import  ClassifySerializer,UserSerializer,ShopSerializer, \
        ProductSerializer,UnLicenseShoperSerializer,LicenseShoperSerializer,SrvLimitSerializer, \
        AreaSerializer,MyShopSerializer,CitySerializer,DistrictSerializer,AddrSerializer,MyAddrSerializer,    \
        OrderSerializer,MyOrderSerializer,UserCommentSerializer,AllCommentSerializer,MyShopSerializer



from rest_framework.renderers import JSONRenderer
from help_get_home.models import *
import datetime
import os
import json
import sys
import ImageFile  
from PIL import Image
import django.forms as forms  
import sys
import re
from collections import OrderedDict 
reload(sys)
sys.setdefaultencoding('utf-8')

class ArgumentException(Exception):
    def __init__(self,errors):
        Exception.__init__(self)
        self.errors = errors
class TokenException(Exception):
    def __init__(self,errors):
        Exception.__init__(self)
        self.errors = errors
def createtoken(phone):
    try:  
        user = User.objects.get(username = phone)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            if not created:
                key = default_token_generator.make_token(user)
                created = datetime.datetime.now()
                Token.objects.filter(user=user).update(key=key,created=created)
                return key
            return token.key
        else:
            return "not user"
    except Exception, e:  
        return str(e)

def checktoken(user_id,key):
    try:
        token = Token.objects.get(user_id=user_id,key=key)
        return True
    except Token.DoesNotExist, e :
        raise Exception("token not exists")
    except Exception, e:
        raise Excetion("token exception:" + str(e))
  
class PictureForm(forms.Form):   
    imagefile = forms.ImageField()  
def image(request,name):
    ext = name.split(".")[-1] # Gather extension
    cType = {"png":"images/png","jpg":"images/jpeg","gif":"images/gif"}
    dir=os.listdir('./images')
    for subdir in dir:
        print "subdir=%s" % subdir
        if name in dir:  # Security
           return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
    else:
        HttpResponse("not found")
def index(request):
    return HttpResponse(_(u"Hello, world."))
def getrollad(request):
    return HttpResponse(u"测试")
def userfeedback(request,user_id,msg_type,msg):
    feedback=UserFeedback(user_id=user_id,message=msg,type=msg_type,status=1,last_modify= datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ));
    feedback.save();
    data = '{"result":"意见反馈成功"}' 
    response=json.loads(data)
    return HttpResponse(json.dumps(response, ensure_ascii=False))  
'''
@api_view(['GET','POST'])
def addimage(request):  
    if request.method == 'POST':  
        form = PictureForm(request.POST, request.FILES)  
        if form.is_valid():  
            f = request.FILES["imagefile"]  
            parser = ImageFile.Parser()  
            for chunk in f.chunks():  
                parser.feed(chunk)  
                img = parser.close()  
                # 在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作  
                img.save("./static/images/")
                return HttpResponse("上传成功")
    else:
        uf = PictureForm()
        return render_to_response('addimage.html',{'uf':uf})
'''
@api_view(['GET','POST'])
def uploadimage(request): 
    if request.method == 'POST':  
        content = request.content_type
        try:
            img = Image.open(content)
            #img.thumbnail((500,500),Image.ANTIALIAS)#对图片进行等比缩放
            img.save("./help_get_home/static/images/abc.jpg")#保存图片 
        except Exception,e:
            return HttpResponse("Error %s"%e)
        return HttpResponse("ok")
    else:
        return render_to_response('uploadimage.html')
@api_view()
def getsrvtype(request,srv_type):
    classify_info = ClassifyInfo.objects.filter(type=srv_type)
    response=OrderedDict()
    if classify_info :
        serializer = ClassifySerializer(classify_info,many = True)
        response['result'] = 'success' 
        response['data'] = serializer.data
    else:
        response['result'] = '没有对应的分类信息'
        response['data'] = classify_info
    json= JSONRenderer().render(response)
    return HttpResponse(json)
@api_view()
def getareainfo(request):
    response =  OrderedDict()
    try:
        area_infos = AreaInfo.objects.filter(status=1)
        if area_infos:
            serializer = AreaSerializer(area_infos,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = 'failed'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = ''
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view()
def getshopinfo(request,srv_sub_type,sort_type,page_num,page_size):
    column_name = ['composite','-srv_attitude','-srv_contents','-srv_speed','-order_num','-recommend']
    response =  OrderedDict()
    try:
        shop_info = []
        user_id = ""
        key = ""
        user_id = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(user_id,key)
        m1 = re.match(r'(^\d{1,2}$)',srv_sub_type)
        m2 = re.match(r'(^\d{1,2}$)',sort_type)
        m3 = re.match(r'(^\d+$)',page_num)
        m4 = re.match(r'(^\d+$)',page_size)
        if m1 == None  :
            raise ArgumentException("invalid argument:srv_sub_type") 
        if m2 == None  :
            raise ArgumentException("invalid argument:sort_type") 
        if m3 == None  :
            raise ArgumentException("invalid argument:page_num") 
        if m4 == None  :
            raise ArgumentException("invalid argument:page_size") 
        if sort_type == '0':
            shop_info = ShopInfo.objects.filter(srv_sub_type__contains=srv_sub_type,verify_status=1,status=1)
        else:
            shop_info = ShopInfo.objects.filter(srv_sub_type__contains=srv_sub_type,verify_status=1,status=1).order_by(column_name[int(sort_type)])
        if  int(page_num)==0  and int(page_size)==0:
            page_size = shop_info.count()
            page_num = 1
        if shop_info:
            p = Paginator(shop_info,page_size)   
            if int(page_num) > p.num_pages:    
                response['result'] = '当前是最后一页,没有多余数据'
            else:
                serializer = ShopSerializer(p.page(page_num),many = True)
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '该类型服务暂时没相关店铺，敬请期待'
            response['data'] = shop_info
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view()
def login(request,phone,password):
    response = OrderedDict()
    try:
        m = re.match(r'(^\d{11}$)',phone)
        if m:
            user_info =  UserInfo.objects.filter(phone=phone)
            if user_info :
                if password == user_info[0].pwd:
                    auth_user = User.objects.get(username=phone)
                    auth_user.last_login = datetime.datetime.now()
                    auth_user.save()
                    key = createtoken(phone)
                    response['result'] = 'success'
                    response['user_id'] = user_info[0].user_id
                    response['key'] = key
                else: 
                    response['result'] = '用户名或密码错误'
            else:
                response['result'] = '用户名或密码错误'

        else:
            response['result'] = '手机号不正确'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('user_id'):
            response['user_id'] = 0
        if not response.has_key('key'):
            response['key'] = ""
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        response = OrderedDict()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                user_info = UserInfo.objects.get(phone=request.data["phone"])
                auth_user = User(id=user_info.user_id,username=request.data['phone'],   \
                                 password=request.data['pwd'], \
                                 is_staff=1,is_active=1,is_superuser=0)
                auth_user.save()
                key = createtoken(request.data['phone'])
                response['result'] = 'success'
                response['user_id'] = user_info.user_id 
                response['key'] = key
            except UserInfo.DoesNotExist:
                response['result'] = 'db error'
                response['user_id'] = 0
        else:
            response['result'] = '用户已存在'
            response['user_id'] = 0
        if not response.has_key('key'):
            response['key'] = ''
        json= JSONRenderer().render(response)
        return HttpResponse(json)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def unlicenseshoper(request):
    if request.method == 'POST':
        response = OrderedDict()
        try:
            serializer = UnLicenseShoperSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                user_info = UserInfo.objects.get(user_id = request.data['user_id'])
                user_info.type = 1
                user_info.save()
                response['result'] = 'success'
            else:
                response['result'] = '注册成为商家失败'
        except Exception, e:
            response['result'] = str(e)
        finally:
            json= JSONRenderer().render(response)
            return HttpResponse(json)
    elif request.method == 'GET' :
        shop_infos = ShopInfo.objects.all()
        serializer = ShopSerializer(shop_infos,many = True)
        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content)
 

    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
@api_view(['POST'])
def licenseshoper(request):
    if request.method == 'POST':
        response = OrderedDict()
        try:
            serializer = LicenseShoperSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                user_info = UserInfo.objects.get(user_id = request.data['user_id'])
                user_info.type = 1
                user_info.save()
                response['result'] = 'success'
            else:
                response['result'] = '注册成为商家失败'
        except Exception, e:
            response['result'] = str(e)
        json= JSONRenderer().render(response)
        return HttpResponse(json)
    elif request.method == 'GET' :
        shop_infos = ShopInfo.objects.all()
        serializer = ShopSerializer(shop_infos,many = True)
        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content)
 

    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'POST'])
def resetpwd(request):
    data = JSONParser().parse(request)
    ret='{"result":"重置密码失败,用户不存在"}'
    try:
        user_info = UserInfo.objects.get(phone=data["phone"])
    except UserInfo.DoesNotExist:
        response=json.loads(ret)
        return HttpResponse(json.dumps(response, ensure_ascii=False))  
    if request.method == 'GET':
        user_infos= UserInfo.objects.all()
        serializer = UserSerializer(user_infos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(user_info,data=data)
        if serializer.is_valid():
            serializer.save()
            ret='{"result":"success"}'
        response=json.loads(ret)
        return HttpResponse(json.dumps(response, ensure_ascii=False))  
       
def getverifycode(request,phone,srv_type):
    data='{"result":"验证码已经发送"}'
    response=json.loads(data)
    return HttpResponse(json.dumps(response, ensure_ascii=False))  

def checkverifycode(request,phone,srv_type,sms_code):
    data='{"result":"success"}'
    response=json.loads(data)
    return HttpResponse(json.dumps(response, ensure_ascii=False))  

@api_view(['GET',])
def getagreement(request):
    t = loader.get_template('index.html')
    c = Context({}) 
    return HttpResponse(t.render(c))
@api_view(['GET',])
def getshoperagreement(request):
    t = loader.get_template('shoper_agreement.html')
    c = Context({}) 
    return HttpResponse(t.render(c))
@api_view()
def srvlimit(request,shoper_type):
    response = OrderedDict()
    try:
        m = re.match(r'(^\d{1,2}$)',shoper_type)
        if m == None:
            raise ArgumentException("invalid argument:shoper_type") 
        srv_limit = SrvLimit.objects.filter(type=shoper_type)
        if srv_limit :
            serializer = SrvLimitSerializer(srv_limit,many = True)
            response['result'] = 'success' 
            response['data'] = serializer.data
        else:
            response['result'] = '没有对应类型的商家'
    except ArgumentException, e:
        response['result'] = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = srv_limit
        json= JSONRenderer().render(response)
        return HttpResponse(json)
class ClassifyViewSet(viewsets.ModelViewSet):
    queryset = ClassifyInfo.objects.filter(type=1)
    serializer_class =  ClassifySerializer                                                                        
    @list_route()
    def getclassify(self,request):
        return Response({'status': 'password set'})
    @detail_route(methods=['post'])
    def post(self, request, format=None):
        serializer = ClassifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializer
    @list_route()
    def getuserinfo(self,request,phone):
        queryset =  UserInfo.objects.filter(phone=phone)
        serializer_class = UserSerializer
        return Response(serializer.data)
    @detail_route(methods=['post'])
    def post(self, request, format=None):
        serializer = ClassifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
**********************商品相关接口************************
'''
'''
**********************商品展示界面***********************

'''
@api_view()
def getshopproduct(request,shop_id,sort_type,page_num,page_size):
    response =  OrderedDict()
    column_name = ['composite','-sales','-evaluate']
    try:
        product_info = []
        user_id = ""
        key = ""
        user_id = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(user_id,key)
        m1 = re.match(r'(^\d{1,2}$)',shop_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:shop_id") 

        m2 = re.match(r'(^\d{1,2}$)',sort_type)
        if m2 == None  :
            raise ArgumentException("invalid argument:sort_type") 

        m3 = re.match(r'(^\d{1,2}$)',page_num)
        if m3 == None  :
            raise ArgumentException("invalid argument:page_num") 

        m4 = re.match(r'(^\d{1,2}$)',page_size)
        if m4 == None  :
            raise ArgumentException("invalid argument:page_size") 
        if int(sort_type) <>  0:
            product_info = ProductInfo.objects.filter(shop_id=shop_id,verify_status=1,status=1).order_by(column_name[int(sort_type)])
        else:
            product_info =  ProductInfo.objects.filter(shop_id=shop_id,verify_status=1,status=1)
        if  int(page_num)==0  and int(page_size)==0:
            page_size = product_info.count()
            page_num = 1
        if product_info:
            p = Paginator(product_info,page_size)   
            if int(page_num) > p.num_pages:    
                response['result'] = '当前是最后一页,没有多余数据'
            else:
                serializer = ProductSerializer(p.page(page_num),many = True)
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '此类商品还未上线，敬请期待'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = product_info
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
******************************商品详细介绍界面*******************************
'''

@api_view()
def getproductbyid(request,product_id):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,9}$)',product_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:product_id") 

        product_info = ProductInfo.objects.filter(product_id=product_id,verify_status=1,status=1)
        if product_info:
            serializer = ProductSerializer(product_info,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = '没有对应的商品信息'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = product_info
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
******************************我的店铺信息界面******************************
'''


@api_view()
def getmyshop(request,user_id):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',user_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        shop_info = ShopInfo.objects.filter(user_id=user_id,verify_status=1,status=1)
        if shop_info:
            serializer = MyShopSerializer(shop_info,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = '该用户没有相应的店铺'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = shop_info
        json= JSONRenderer().render(response)
        return HttpResponse(json)

'''
**********************我的店铺商品界面***********************

'''

@api_view()
def getproductbyshop(request,shop_id,page_num,page_size):
    response =  OrderedDict()
    try:
        product_info = []
        user_id = ""
        key = ""
        user_id = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(user_id,key)
        m1 = re.match(r'(^\d{1,2}$)',shop_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:shop_id") 

        m2 = re.match(r'(^\d{1,2}$)',page_num)
        if m2 == None  :
            raise ArgumentException("invalid argument:page_num") 

        m3 = re.match(r'(^\d{1,2}$)',page_size)
        if m3 == None  :
            raise ArgumentException("invalid argument:page_size") 
        product_info = ProductInfo.objects.filter(shop_id=shop_id,verify_status=1,status=1)
        if  int(page_num)==0  and int(page_size)==0:
            page_size = product_info.count()
            page_num = 1
        if product_info:
            p = Paginator(product_info,page_size)   
            if int(page_num) > p.num_pages:    
                response['result'] = '当前是最后一页,没有多余数据'
            else:
                serializer = ProductSerializer(p.page(page_num),many = True)
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '店铺商品还未上线，敬请期待'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = product_info
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**********************************我的店铺编辑资料界面*************************
'''
@api_view(['POST'])
def updatemyshopinfo(request):
    response =  OrderedDict()
    try:
        user_id = ""
        key = ""
        user_id = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(user_id,key)
        myshop_info = ShopInfo.objects.get(shop_id=request.data["shop_id"])
        serializer = MyShopSerializer(myshop_info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ShopInfo.DoesNotExist:
        response['result'] = '店铺信息不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**************************城市选择界面*******************************
'''

@api_view()
def getcityinfo(request):
    response =  OrderedDict()
    try:
        city_infos = CityInfo.objects.filter(status=1)
        if city_infos:
            serializer = CitySerializer(city_infos,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = 'failed'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = city_infos
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**********************行政区选择界面**********************************
'''
@api_view()
def getdistrictinfo(request,city_id):
    response =  OrderedDict()
    try:
        district_infos = DistrictInfo.objects.filter(city_id=city_id,status=1)
        if district_infos:
            serializer = DistrictSerializer(district_infos,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = 'failed'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = district_infos
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**************************我的地址编辑界面*******************************
'''

@api_view()
def getmyaddrinfo(request,user_id):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        addr_infos= []
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        if uid<>user_id:
            raise Exception,"Permission Denied"
        checktoken(uid,key)
        m1 = re.match(r'(^\d{1,11}$)',user_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        addr_infos = AddrInfo.objects.filter(user_id=user_id,status=1)
        if len(addr_infos):
            serializer = MyAddrSerializer(addr_infos,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = '未添加相应地址信息'
    except KeyError, e:
        response['result'] = 'not authorization'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = addr_infos
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
************************新增我的地址界面*********************************
'''

@api_view(['POST'])
def addmyaddress(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        addr_infos= []
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        if int(uid)<>request.data["user_id"]:
            raise Exception,"Permission Denied"
        checktoken(uid,key)
        serializer = AddrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
        else:
            response['result'] = str(serializer.errors)
    except KeyError, e:
        response['result'] = 'not authorization'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
************************编辑地址界面*********************************
'''

@api_view(['POST'])
def updatemyaddress(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        if int(uid)<>request.data["user_id"]:
            raise Exception,"Permission Denied"
        checktoken(uid,key)
        addr_info = AddrInfo.objects.get(id=request.data["id"])
        serializer =AddrSerializer(addr_info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
        else:
            response['result'] = str(serializer.errors)
    except KeyError, e:
        response['result'] = 'not authorization'
    except AddrInfo.DoesNotExist:
        response['result'] = '地址不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**********************判断用户是否已经是商家**********************************
'''
@api_view()
def checkisshoper(request,user_id):
    shoper_status={'0':'未审核','1':'审核通过','2':'审核不通过，请重新提交资料'}
    response =  OrderedDict()
    m1 = re.match(r'(^\d{1,11}$)',user_id)
    if m1 == None  :
        raise ArgumentException("invalid argument:user_id") 
    try:
        shop_info = ShopInfo.objects.get(user_id=user_id,status=1)
        response['result'] = shoper_status[str(shop_info.verify_status)]
    except ShopInfo.DoesNotExist, e:
            response['result'] = '用户未注册成为商家'
    except Exception, e:
        response['result'] = str(e)
    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
************************店铺与服务介绍编辑界面*********************************
'''

@api_view(['POST'])
def updateshopdesc(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        shop_info = ShopInfo.objects.get(shop_id=request.data['shop_id'])
        if int(uid)<>shop_info.user_id:
            raise Exception,"Permission Denied"
        shop_info.shop_desc = request.data['shop_desc']
        shop_info.save()
        response['result'] = 'success'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ShopInfo.DoesNotExist:
        response['result'] = '店铺不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
************************我的店铺信息编辑界面：编辑图标*********************************
'''

@api_view(['POST'])
def updateshopicon(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        shop_info = ShopInfo.objects.get(shop_id=request.data['shop_id'])
        if int(uid)<>shop_info.user_id:
            raise Exception,"Permission Denied"
        shop_info.shop_url = request.data['shop_url']
        shop_info.save()
        response['result'] = 'success'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ShopInfo.DoesNotExist:
        response['result'] = '店铺不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
************************往购物车增加商品*********************************
'''

@api_view(['POST'])
def addorder(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        if int(uid)<>request.data["user_id"]:
            raise Exception,"Permission Denied"
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            product_info = ProductInfo.objects.get(product_id = request.data['product_id'])
            product_info.product_num = product_info.product_num - 1
            product_info.save()
            response['result'] = 'success'
        else:
            response['result'] = 'order_id 不正确'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**************************我的订单管理*******************************
'''

@api_view()
def getmyorder(request,user_id,order_status):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',user_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        m2 = re.match(r'([0-3])',order_status)
        if m2 == None  :
            raise ArgumentException("invalid argument:order_status") 
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        if uid<>user_id:
            raise Exception,"Permission Denied"
        order_infos = SaleOrder.objects.filter(user_id=user_id,order_status=order_status,status=1)
        order_list=[]
        if order_infos:
            for temp in order_infos:
                order_dict = OrderedDict()
                order_dict['order_id'] = temp.order_id
                order_dict['order_status'] = temp.order_status  
                product_info = ProductInfo.objects.get(product_id=temp.product_id)
                order_dict['product_url'] = product_info.url
                order_dict['product_name'] = product_info.product_name
                shop_info = ShopInfo.objects.get(shop_id=temp.shop_id)
                order_dict['shop_name'] = shop_info.shop_name
                order_dict['telephone'] = shop_info.telephone
                addr_info = AddrInfo.objects.get(id=temp.address_info)
                order_dict['addr_info'] = addr_info.district + addr_info.area + addr_info.address
                order_dict['price'] = temp.money
                order_dict['product_num'] = temp.product_num
                order_list.append(order_dict)
            serializer = MyOrderSerializer(data=order_list,many = True)
            if serializer.is_valid():
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '没有相应的订单'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
*******************************订单状态修改************************************
'''
 
@api_view(['POST'])
def updateorderstatus(request):
    response =  OrderedDict()
    current_status = {'1':0,'2':1,'3':2}
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        next_status = str(request.data['order_status'])
        m= re.match(r'([0-3])',next_status)
        if m == None  :
            raise ArgumentException("invalid argument:order_status only can be 0-3") 
        order_info = SaleOrder.objects.get(order_id=request.data['order_id'],status=1)
        if int(uid)<>order_info.user_id:
            raise Exception,"Permission Denied"
        if order_info.order_status <> current_status[next_status]:
            response['result'] = '当前订单状态不支持此操作'
        else:
            order_info.order_status = request.data['order_status']
            order_info.save()
            response['result'] = 'success'
            if next_status=='1':
                product_info = ProductInfo.objects.get(product_id = order_info.product_id)
                product_info.sales = product_info.sales + 1
                product_info.save()
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except SaleOrder.DoesNotExist:
        response['result'] = '订单不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
*****************************从购物车删除订单*********************************
'''
@api_view(['POST'])
def updateshoppingcart(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        status = str(request.data['status'])
        m= re.match(r'([0-1])',status)
        if m == None  :
            raise ArgumentException("invalid argument:status only can be 0-1") 
        order_info = SaleOrder.objects.get(order_id=request.data['order_id'])
        if int(uid)<>order_info.user_id:
            raise Exception,"Permission Denied"
        order_info.status = request.data['status']
        order_info.save()
        response['result'] = 'success'
        product_info = ProductInfo.objects.get(product_id = order_info.product_id)
        if status=='0':
            product_info.product_num = product_info.product_num + 1
        if status=='1':
            product_info.product_num = product_info.product_num - 1
        product_info.save()
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except SaleOrder.DoesNotExist:
        response['result'] = '订单不存在'
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
***********************************商家订单管理界面**************************
'''
@api_view()
def getshoperorder(request,user_id,order_status):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',user_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        m2 = re.match(r'([0-3])',order_status)
        if m2 == None  :
            raise ArgumentException("invalid argument:order_status") 
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        if uid<>user_id:
            raise Exception,"Permission Denied"
        shop_infos = ShopInfo.objects.filter(user_id=user_id)
        shop_list=[]
        for myshop in shop_infos:
            shop_list.append(myshop.shop_id)
        if order_status==1:
            order_infos = SaleOrder.objects.filter(shop_id__in=shop_list,order_status=order_status,status=1,c_time__gt=datetime.datetime.now().date())
        else:
            order_infos = SaleOrder.objects.filter(shop_id__in=shop_list,order_status=order_status,status=1)
        order_list=[]
        if order_infos:
            for temp in order_infos:
                order_dict = OrderedDict()
                order_dict['order_id'] = temp.order_id
                order_dict['order_status'] = temp.order_status  
                product_info = ProductInfo.objects.get(product_id=temp.product_id)
                order_dict['product_url'] = product_info.url
                order_dict['product_name'] = product_info.product_name
                shop_info = ShopInfo.objects.get(shop_id=temp.shop_id)
                order_dict['shop_name'] = shop_info.shop_name
                order_dict['telephone'] = shop_info.telephone
                addr_info = AddrInfo.objects.get(id=temp.address_info)
                order_dict['addr_info'] = addr_info.district + addr_info.area + addr_info.address
                order_dict['price'] = temp.money
                order_dict['product_num'] = temp.product_num
                order_list.append(order_dict)
            serializer = MyOrderSerializer(data=order_list,many = True)
            if serializer.is_valid():
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '没有相应的订单'
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
****************************服务评价界面*******************************
'''
@api_view(['POST'])
def addusercomment(request):
    response =  OrderedDict()
    try:
        serializer = UserCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
        else:
            response['result'] = '数据格式错误'
            response['error_info'] = str(serializer.errors)
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
****************************用户评价界面界面****************************
'''
@api_view()
def getusercomment(request,user_id):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',user_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        shop_infos = ShopInfo.objects.filter(user_id=user_id)
        shop_list=[0]
        #for myshop in shop_infos:
        shop_list.append(shop_infos[0].shop_id)
        user_comments = UserComment.objects.filter(shop_id__in=shop_list,status=1)
        comment_list=[]
        if user_comments:
            for temp in user_comments:
                comment_dict = OrderedDict()
                user_info = UserInfo.objects.get(temp.user_id)
                comment_dict['comment_id'] = temp.id
                comment_dict['user_nick'] = user_info.nick
                comment_dict['match_desc'] = temp.match_desc
                comment_dict['comment'] = temp.comment
                comment_list.append(comment_dict)
            serializer = AllCommentSerializer(data=comment_list,many = True)
            if serializer.is_valid():
                response['result'] = 'success'
                response['data'] = serializer.data
        else:
            response['result'] = '没有相应的评论'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = ''
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view()
def display_meta(request):
    values = request.META.items()
    values.sort()    
    html = []    
    for k, v in values:        
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))    
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

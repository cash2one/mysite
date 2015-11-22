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
        OrderSerializer,MyOrderSerializer,UserCommentSerializer,AllCommentSerializer,MyShopSerializer,    \
        AdSerializer,ShoppingCartSerializer



from rest_framework.renderers import JSONRenderer
from help_get_home.models import *
from help_get_home.wxzhifu import *
from help_get_home.sendsms import *
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
  
def checkcode(phone,type,code):
    try:
        verify_code = VerifyCode.objects.get(phone=phone,type=type,code=code)
        return True
    except VerifyCode.DoesNotExist:
        return False
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
    feedback=UserFeedback(user_id=user_id,message=msg,type=msg_type,status=1,last_modify= datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ));
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
    response=OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,2}$)',srv_type)
        if m1 == None  :
            raise Exception,"invalid argument:srv_sub_type" 
        parent_info = ClassifyInfo.objects.get(id = srv_type)
        classify_info = ClassifyInfo.objects.filter(parent_id=srv_type)
        data=[]
        if classify_info :
            for temp in classify_info:
                classify_dict = OrderedDict()
                classify_dict["type"] = int(srv_type)
                classify_dict["label"] = parent_info.name
                classify_dict["sub_type"] = temp.id
                classify_dict["sub_label"] = temp.name
                data.append(classify_dict)
            response['result'] = 'success' 
            response['data'] = data
        else:
            response['result'] = '没有对应的分类信息'
            response['data'] = []
    except ClassifyInfo.DoesNotExist:
        response['result'] = '没有对应分类信息'
        response['data'] = []
    except Exception, e:
        response['result'] = 'failed'
        response['data'] = str(e)
    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view()
def getareainfo(request,city,district):
    response =  OrderedDict()
    try:
        area_infos = AreaInfo.objects.filter(parent_id=district,status=1)
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
        regionCode = ""
        user_id = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        regioncode = request.META['HTTP_REGIONCODE']
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
            shop_info = ShopInfo.objects.filter(srv_sub_type__contains=srv_sub_type,srv_community__contains=regioncode,verify_status=1,status=1)
        else:
            shop_info = ShopInfo.objects.filter(srv_sub_type__contains=srv_sub_type,srv_community__contains=regioncode,verify_status=1,status=1).order_by(column_name[int(sort_type)])
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
@api_view(['POST'])
def login(request):
    response = OrderedDict()
    try:
        phone = str(request.data['phone'])
        m = re.match(r'(^\d{11}$)',phone)
        if m:
            password = request.data['password']
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
                    response['user'] = phone
                    response['pwd'] = password
            else:
                response['result'] = '用户名或密码错误:usr_info is null'

        else:
            response['user'] = phone
            response['pwd'] = password
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
    response = OrderedDict()
    try:
        phone = request.data["phone"]
        verify_code = request.data["verify_code"]
        pwd = request.data["pwd"]
        if not checkcode(phone,1,verify_code): 
            raise Exception,"验证码错误"
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_info = UserInfo.objects.get(phone=phone)
            auth_user = User(id=user_info.user_id,username=phone,   \
                                 password=pwd, \
                                 is_staff=1,is_active=1,is_superuser=0)
            auth_user.save()
            key = createtoken(phone)
            response['result'] = 'success'
            response['user_id'] = user_info.user_id 
            response['key'] = key
        else:
            response['result'] = '用户已存在'
    except Exception, e:
        response['result'] = str(e)
    except UserInfo.DoesNotExist:
        response['result'] = 'db error'
    finally:
        if not response.has_key('key'):
            response['key'] = ''
        if not response.has_key('user_id'):
            response['user_id'] = 0
        json= JSONRenderer().render(response)
        return HttpResponse(json)

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
       
@api_view()
def getverifycode(request,phone,type):
    response = OrderedDict()
    try:
        m = re.match(r'(^\d{11}$)',phone)
        if m == None:
            raise ArgumentException("invalid argument:phone") 
        tpl_id = '7231' #申请的短信模板ID,根据实际情况修改 
        tpl_value = '#app#=bang&#code#=' #短信模板变量,根据实际情况修改
        code = Common_util_pub().createverifycode()
        tpl_value=tpl_value+code
        verify_code=VerifyCode.objects.get(phone=phone,type=type)
        verify_code.code=code
        verify_code.last_modify = datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )
        verify_code.save()
        sendsms(phone, tpl_id, tpl_value) #请求发送短信
        response["result"] = "验证码已发送"
    except ArgumentException, e:
        response['result'] = e.errors
    except VerifyCode.DoesNotExist:
        verify_code=VerifyCode(phone=phone,code=code,type=type,last_modify= datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S' ));
        verify_code.save()
        sendsms(phone, tpl_id, tpl_value) #请求发送短信
        response["result"] = "验证码已发送"
    except Exception, e:
        response['result'] = str(e)
    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)

@api_view()
def checkverifycode(request,phone,type,code):
    response = OrderedDict()
    try:
        m = re.match(r'(^\d{11}$)',phone)
        if m == None:
            raise ArgumentException("invalid argument:phone") 
        if checkcode(phone,type,code):
            response["result"] = "success"
        else:
            response["result"] = "fail"
    except ArgumentException, e:
        response['result'] = e.errors
    except Exception, e:
        response['result'] = "fail"
    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)

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
            response['data'] = []
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
        city_infos = AreaInfo.objects.filter(parent_id=0,status=1)
        if city_infos:
            serializer = AreaSerializer(city_infos,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = 'failed'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**********************行政区选择界面**********************************
'''
@api_view()
def getdistrictinfo(request,city_id):
    response =  OrderedDict()
    try:
        area_infos = AreaInfo.objects.filter(parent_id=city_id,status=1)
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
            response['data'] = []
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
"""
*=======================================================================
*统一下单
*=======================================================================
"""
def unifiedorder(out_trade_no,body,total_fee):
    c = HttpClient()
    c2 = HttpClient()
    assert id(c) == id(c2)
    unifiedorder = UnifiedOrder_pub()
    unifiedorder.setParameter("out_trade_no",out_trade_no)
    unifiedorder.setParameter("body",body)
    unifiedorder.setParameter("total_fee",total_fee)
    unifiedorder.setParameter("notify_url","http://wxpay.weixin.qq.com/pub_v2/pay/notify.v2.php")
    unifiedorder.setParameter("trade_type","APP")
    result = unifiedorder.getPrepayId()
    return result
    print "*************统一下单result******************"
    print "====================================="
    print "%s" % result
    print "====================================="
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
        order_info={}
        order_info["user_id"] = request.data["user_id"]
        order_info["total"] = request.data["total"]
        order_info["real_total"] = request.data["real_total"]
        order_info["pay_type"] = request.data["pay_type"]
        order_info["coupon_id"] = request.data["coupon_id"]
        order_info["address_info"] = request.data["address_info"]
        order_id = "order-" +  Common_util_pub().createOrderId()
        order_info['order_id'] = order_id
        body=""
        shopping_cart = request.data["shopping_cart"]
        for temp in shopping_cart:
            shopping_cartid=temp["shopping_cartid"]
            shopping_cart_info = ShoppingCart.objects.get(shopping_cartid=shopping_cartid)
            shopping_cart_info.order_id=order_id
            shopping_cart_info.status=0
            shopping_cart_info.save()
            product_info = ProductInfo.objects.get(product_id = shopping_cart_info.product_id)
            product_info.product_num = product_info.product_num - 1
            product_info.save()
            body=body+"|"+product_info.product_name
        prepayid=unifiedorder(order_id,body,str(order_info["real_total"]))
        order_info["prepayid"] = prepayid
        serializer = OrderSerializer(data=order_info)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
            response['order_id'] = order_info["order_id"]
        else:
            response['result'] = serializer.errors
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception,e:
        response['result'] = str(e)

    finally:
        if not response.has_key('order_id'):
            response['order_id'] = ""
        json= JSONRenderer().render(response)
        return HttpResponse(json)
"""
*=======================================================================
*统一下单
*=======================================================================
"""
@api_view()
def getpayreq(request,order_id,pay_type):
    response = OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        data = OrderedDict()
        wxpay_conf = WxPayConf_pub()
        common_util = Common_util_pub()
        data["appid"] = wxpay_conf.APPID
        data["partnerid"] = wxpay_conf.MCHID
        data["package"] = "WXPay"
        data["noncestr"] = common_util.createNoncestr()
        data["timestamp"] = str(int(time.time())) 
        order_info = SaleOrder.objects.get(order_id=order_id)
        prepayid = order_info.prepayid
        if prepayid is None :
            product_info = ProductInfo.objects.get(product_id = order_info.product_id)
            prepayid=unifiedorder(order_info.order_id,product_info.product_name,str(order_info.money))
            order_info.prepayid=prepayid
            order_info.save()
        data["prepayid"] = prepayid
        sign = common_util.getSign(data)
        data["sign"] = sign
        response["result"] = "success"
        response["data"] = data
    except KeyError, e:
        response['result'] = 'not authorization'
    except SaleOrder.DoesNotExist:           
        response['result'] = "fail"
    except Exception,e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
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
                order_dict['real_total'] = temp.real_total
                addr_info = AddrInfo.objects.get(id=temp.address_info)
                order_dict['addr_info'] = addr_info.district + addr_info.area + addr_info.address
                shopping_cart = ShoppingCart.objects.filter(order_id=temp.order_id)
                order_dict['detail'] =[]
                for cart_info in shopping_cart:
                    detail = OrderedDict()
                    product_info = ProductInfo.objects.get(product_id=cart_info.product_id)
                    detail['product_url'] = product_info.url
                    detail['product_name'] = product_info.product_name
                    detail['product_num'] = cart_info.product_num
                    shop_info = ShopInfo.objects.get(shop_id=cart_info.shop_id)
                    detail['shop_name'] = shop_info.shop_name
                    detail['telephone'] = shop_info.telephone
                    order_dict['detail'].append(detail)
                order_list.append(order_dict)
            response['result'] = 'success'
            response['data'] = order_list
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
        #checktoken(uid,key)
        if uid<>user_id:
            raise Exception,"Permission Denied"
        shop_infos = ShopInfo.objects.filter(user_id=user_id)
        if shop_infos is None:
            raise Exception,"用户未注册店铺"
        shop_ids=[]
        for myshop in shop_infos:
            shop_ids.append(myshop.shop_id)
        cart_infos = ShoppingCart.objects.exclude(order_id="").filter(user_id=user_id)

        if cart_infos is None:
            raise Exception,"该商家没有订单"

        order_ids = []
        for order_id in order_ids:
            order_ids.append(order_id)

        if order_status==1:
            order_infos = SaleOrder.objects.filter(order_id__in=order_ids,order_status=order_status,status=1,c_time__gt=datetime.datetime.now().date())
        else:
            order_infos = SaleOrder.objects.filter(order_id__in=order_ids,order_status=order_status,status=1)
        order_list=[]
        if order_infos:
            for temp in order_infos:
                order_dict = OrderedDict()
                order_dict['order_id'] = temp.order_id
                order_dict['order_status'] = temp.order_status  
                order_dict['real_total'] = temp.real_total
                addr_info = AddrInfo.objects.get(id=temp.address_info)
                order_dict['addr_info'] = addr_info.district + addr_info.area + addr_info.address
                shopping_cart = ShoppingCart.objects.filter(order_id=temp.order_id)
                order_dict['detail'] =[]
                for cart_info in shopping_cart:
                    detail = OrderedDict()
                    product_info = ProductInfo.objects.get(product_id=cart_info.product_id)
                    detail['product_url'] = product_info.url
                    detail['product_name'] = product_info.product_name
                    detail['product_num'] = cart_info.product_num
                    shop_info = ShopInfo.objects.get(shop_id=cart_info.shop_id)
                    detail['shop_name'] = shop_info.shop_name
                    detail['telephone'] = shop_info.telephone
                    order_dict['detail'].append(detail)
                order_list.append(order_dict)
            response['result'] = 'success'
            response['data'] = order_list
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
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        if int(uid)<>request.data["user_id"]:
            raise Exception,"Permission Denied"
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
def getusercomment(request,product_id):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',product_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:user_id") 
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        user_comments = UserComment.objects.filter(product_id=product_id,status=1)
        comment_list=[]
        if user_comments:
            for temp in user_comments:
                comment_dict = OrderedDict()
                user_info = UserInfo.objects.get(user_id=temp.user_id)
                comment_dict['comment_id'] = temp.id
                comment_dict['user_nick'] = user_info.nick
                comment_dict['match_desc'] = temp.match_desc
                comment_dict['comment'] = temp.comment
                comment_dict['last_modify'] = temp.last_modify.strftime("%Y-%M-%d")
                comment_list.append(comment_dict)
            response['result'] = 'success'
            response['data'] = comment_list
        else:
            response['result'] = '没有相应的评论'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
@api_view()
def searchproduct(request,product_name):
    response =  OrderedDict()
    try:

        product_info = ProductInfo.objects.filter(product_name__contains = product_name,verify_status=1,status=1)
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
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
******************************获取首页广告信息******************************
'''


@api_view()
def getad(request,type):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',type)
        if m1 == None  :
            raise ArgumentException("invalid argument:type") 
        ad_info = ActivityInfo.objects.filter(type=type,status=1)
        if ad_info:
            serializer = AdSerializer(ad_info,many = True)
            response['result'] = 'success'
            response['data'] = serializer.data
        else:
            response['result'] = '该类型没有对应广告信息'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
******************************获取首页广告信息详情******************************
'''


@api_view()
def getdetailad(request,activity_id):
    response =  OrderedDict()
    try:
        m1 = re.match(r'(^\d{1,11}$)',activity_id)
        if m1 == None  :
            raise ArgumentException("invalid argument:activity_id") 
        ad_info = ActivityInfo.objects.get(activity_id=activity_id,status=1)
        shop_ids = ActivityShop.objects.filter(activity_id=activity_id,status=1)
        shop_list=[]
        for temp in shop_ids:
            shop_dict = OrderedDict()
            shop_info = ShopInfo.objects.get(shop_id=temp.shop_id)
            shop_dict["shop_id"]=shop_info.shop_id
            shop_dict["shop_name"] = shop_info.shop_name
            shop_dict["shop_url"] = shop_info.shop_url
            shop_list.append(shop_dict)
        response['result'] = 'success'
        response['detail_url'] = ad_info.detail_url
        response['shop_info'] = shop_list
    except ActivityInfo.DoesNotExist:
        response['result']='无效的活动id'
    except ArgumentException, e:
        response['result']  = e.errors
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('detail_url'):
            response['detail_url'] = ""
        if not response.has_key('shop_info'):
            response['shop_info'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
"""
*=======================================================================
*查询订单
*=======================================================================
"""
@api_view()
def orderquery(request,out_trade_no):
    response =  OrderedDict()
    try:
        order_query = OrderQuery_pub()
        order_query.setParameter("out_trade_no",out_trade_no)
        query_result = order_query.getResult()
        response["result"] = "success"
        response["data"] = query_result
        if query_result["return_code"] == "SUCCESS":  
            if query_result["result_code"] == "SUCCESS":
                if query_result["trade_state "] == "SUCCESS":
                    order_info = SaleOrder.objects.get(order_id=out_trade_no,status=1)
                    if order_info.status==0 :
                        order_info.status=1
                        order_info.save()
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)

"""
*=======================================================================
*个人资料
*=======================================================================
"""
@api_view()
def getuserinfo(request,user_id):
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
        data = OrderedDict()
        addr_info = AddrInfo.objects.get(user_id=user_id,status=1,addr_type=1)
        user_info = UserInfo.objects.get(user_id=user_id,status=1)
        data["head_url"] = user_info.head_url
        data["name"] = addr_info.name
        data["address"] = addr_info.address
        data["phone"] = addr_info.telephone
        data["points"] = 0
        response['result'] = 'success'
        response['data'] = data
    except AddrInfo.DoesNotExist:
        response["result"] = "fail"
    except UserInfo.DoesNotExist:
        response["result"] = "fail"
    except KeyError, e:
        response['result'] = 'not authorization'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = []
        json= JSONRenderer().render(response)
        return HttpResponse(json)
"""
*=======================================================================
*上传用户头像
*=======================================================================
"""
@api_view(['POST'])
def uploadheadimg(request):
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
        user_info = UserInfo.objects.get(user_id=uid,status=1)
        user_info.head_url = request.data["head_url"]
        user_info.save()
        response['result'] = 'success'
    except KeyError, e:
        response['result'] = 'not authorization'
    except UserInfo.DoesNotExist:
        response["result"] = "fail"
    except Exception,e:
        response['result'] = str(e)

    finally:
        json= JSONRenderer().render(response)
        return HttpResponse(json)

"""
*=======================================================================
*往购物车添加商品
*=======================================================================
"""
@api_view(['POST'])
def addshoppingcart(request):
    response =  OrderedDict()
    try:
        uid = ""
        key = ""
        uid = request.META['HTTP_USERID']
        key = request.META['HTTP_KEY']
        checktoken(uid,key)
        if int(uid)<>request.data["user_id"]:
            raise Exception,"Permission Denied"
        shopping_cart_info = request.data
        shopping_cart_info['shopping_cartid'] ="shoppingcart-" +  Common_util_pub().createOrderId()
        serializer = ShoppingCartSerializer(data=shopping_cart_info)
        if serializer.is_valid():
            serializer.save()
            response['result'] = 'success'
            response['shopping_cartid'] = shopping_cart_info['shopping_cartid']
        else:
            response['result'] = serializer.errors
    except KeyError, e:
        response['result'] = 'not authorization'
    except ArgumentException, e:           
        response['result'] = e.errors
    except Exception,e:
        response['result'] = str(e)

    finally:
        if not response.has_key('shopping_cartid'):
            response['shopping_cartid'] = ""
        json= JSONRenderer().render(response)
        return HttpResponse(json)
'''
**************************我的购物车界面*******************************
'''

@api_view()
def getmyshoppingcart(request,user_id):
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
        cart_infos =ShoppingCart.objects.filter(user_id=user_id,status=1)
        if len(cart_infos):
            serializer = ShoppingCartSerializer(cart_infos,many = True)
            response['result'] = 'success'
        else:
            response['result'] = '购物车为空'
        data=[]
        for temp in cart_infos:
            detail=OrderedDict()
            detail['shopping_cartid'] = temp.shopping_cartid;
            detail['product_id'] = temp.product_id
            product_info = ProductInfo.objects.get(product_id=temp.product_id)
            detail['product_url'] = product_info.url
            detail['product_name'] = product_info.product_name
            detail['price'] = product_info.price
            detail['product_num'] = temp.product_num
            shop_info = ShopInfo.objects.get(shop_id=temp.shop_id)
            detail['shop_name'] = shop_info.shop_name
            detail['telephone'] = shop_info.telephone
            data.append(detail)
    except KeyError, e:
        response['result'] = 'not authorization'
    except Exception, e:
        response['result'] = str(e)
    finally:
        if not response.has_key('data'):
            response['data'] = data
        json= JSONRenderer().render(response)
        return HttpResponse(json)

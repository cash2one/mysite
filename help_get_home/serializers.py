#conding='utf-8'
#from help_get_home.models import ClassifyInfo,UserInfo,ShopInfo,ProductInfo
#coding=utf-8
default_encoding='utf-8'
from  help_get_home.models import *
from rest_framework import serializers
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

class ClassifySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClassifyInfo
        fields = ('type','label','sub_type','sub_label','status')
class SrvLimitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SrvLimit 
        fields = ('requirement','srv_limit')
class UserSerializer(serializers.HyperlinkedModelSerializer):
    sex = serializers.IntegerField(required=False,default=0)
    address_id = serializers.IntegerField(required=False,default=0)
    type = serializers.IntegerField(required=False,default=0)
    verify_status = serializers.IntegerField(required=False,default=1)
    status = serializers.IntegerField(required=False,default=1)
    class Meta:
        model = UserInfo
        fields = ('phone','pwd','sex','address_id','type','verify_status','status')
class ShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ('shop_id','shop_name','shop_url','type','entity','level', \
                  'shop_address','srv_attitude','srv_speed', \
                  'srv_contents','order_num','shop_desc'
                 )

class MyShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ('shop_id','shop_name','shop_url','srv_sub_type','level' \
                 )
class UnLicenseShoperSerializer(serializers.HyperlinkedModelSerializer):
    srv_attitude = serializers.IntegerField(required=False,default=0)
    srv_speed = serializers.IntegerField(required=False,default=0)
    srv_contents = serializers.IntegerField(required=False,default=0)
    order_num = serializers.IntegerField(required=False,default=0)
    recommend = serializers.IntegerField(required=False,default=0)
    entity = serializers.IntegerField(required=False,default=0)
    level = serializers.IntegerField(required=False,default=1)
    verify_status = serializers.IntegerField(required=False,default=0)
    status = serializers.IntegerField(required=False,default=1)
    last_modify = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    class Meta:
        model = ShopInfo
        fields = ('user_id','shop_name','type', \
                  'shoper','shoper_phone','telephone','srv_sub_type',\
                  'srv_community','shop_address','post_address',\
                  'positive_idcard','opposite_idcard','hand_idcard',   \
                  'srv_attitude','srv_speed','srv_contents','order_num','recommend',  \
                  'entity','level',      \
                  'verify_status','status','last_modify')


class LicenseShoperSerializer(serializers.HyperlinkedModelSerializer):
    shoper_phone = serializers.IntegerField(required=False,default=0)
    srv_attitude = serializers.IntegerField(required=False,default=0)
    srv_speed = serializers.IntegerField(required=False,default=0)
    srv_contents = serializers.IntegerField(required=False,default=0)
    order_num = serializers.IntegerField(required=False,default=0)
    recommend = serializers.IntegerField(required=False,default=0)
    entity = serializers.IntegerField(required=False,default=1)
    level = serializers.IntegerField(required=False,default=1)
    verify_status = serializers.IntegerField(required=False,default=0)
    status = serializers.IntegerField(required=False,default=1)
    last_modify = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    class Meta:
        model = ShopInfo
        fields = ('user_id','shop_name','type', \
                  'shoper','telephone','srv_sub_type',\
                  'srv_community','shop_address',\
                  'positive_idcard','opposite_idcard','hand_idcard', \
                  'business_license','tax_license','shoper_phone',     \
                  'srv_attitude','srv_speed','srv_contents','order_num','recommend',  \
                  'entity','level',                                     \
                  'verify_status','status','last_modify')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('product_id','product_name','shop_id','url','price','product_num','product_desc','begin_time','end_time','evaluate')
class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AreaInfo
        fields = ('area_id','area')
class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CityInfo
        fields = ('city_id','city')
class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DistrictInfo
        fields = ('city_id','district_id','district')
class AddrSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(max_value=None, min_value=None,required=False)
    addr_type = serializers.IntegerField(max_value=None, min_value=None,required=False,default=0)
    status = serializers.IntegerField(required=False,default=1)
    last_modify = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    class Meta:
        model = AddrInfo
        fields = ('id','user_id','name','telephone','city','district','area','address','addr_type','status','last_modify')

class MyAddrSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AddrInfo
        fields = ('id','name','telephone','city','district','area','address','addr_type')
class MyShopSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShopInfo
        fields = ('shop_id','shop_name', \
                  'shop_address','telephone','srv_community')
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_status = serializers.IntegerField(required=False,default=0)
    pay_type = serializers.IntegerField(max_value=2, min_value=0,required=False,default=0)
    is_coupon = serializers.IntegerField(required=False,default=0)
    status = serializers.IntegerField(required=False,default=1)
    c_time = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    m_time = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    class Meta:
        model = SaleOrder
        fields = ('order_id','user_id','product_id','shop_id','product_num', \
                  'money','begin_time','end_time','address_info','order_status',   \
                  'pay_type','is_coupon','status','c_time','m_time'
                  )
class MyOrderSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=64, allow_blank=False, trim_whitespace=True)
    order_status = serializers.IntegerField()
    product_url = serializers.CharField(max_length=128, allow_blank=False, trim_whitespace=True)
    product_name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    shop_name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    telephone = serializers.IntegerField()
    addr_info = serializers.CharField(max_length=128, allow_blank=False, trim_whitespace=True)
    product_num = serializers.IntegerField()
    price = serializers.IntegerField()
class UserCommentSerializer(serializers.HyperlinkedModelSerializer):
    status = serializers.IntegerField(required=False,default=1)
    last_modify = serializers.DateTimeField(required=False,default = datetime.datetime.now)
    class Meta:
        model = UserComment
        fields = ('order_id','user_id','product_id','shop_id', \
                  'comment','match_desc','srv_attitude','srv_speed', \
                  'srv_contents','status','last_modify' \
                  )
class AllCommentSerializer(serializers.Serializer):
    user_nick = serializers.CharField(max_length=64, allow_blank=False, trim_whitespace=True)
    comment_id = serializers.IntegerField()
    match_desc = serializers.IntegerField()
    comment = serializers.CharField(max_length=128, allow_blank=False, trim_whitespace=True)

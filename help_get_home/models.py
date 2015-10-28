# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AddrInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=128, blank=True)
    telephone = models.BigIntegerField()
    city = models.CharField(max_length=128, blank=True)
    district = models.CharField(max_length=128, blank=True)
    area = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    addr_type = models.IntegerField()
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addr_info'


class AreaInfo(models.Model):
    area_id = models.BigIntegerField(primary_key=True)
    area = models.CharField(max_length=500, blank=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_info'


class CityInfo(models.Model):
    city_id = models.BigIntegerField(primary_key=True)
    city = models.CharField(max_length=500, blank=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_info'


class ClassifyInfo(models.Model):
    sub_type = models.IntegerField(primary_key=True)
    type = models.IntegerField(blank=True, null=True)
    label = models.CharField(max_length=64, blank=True)
    sub_label = models.CharField(max_length=64, blank=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classify_info'


class DistrictInfo(models.Model):
    district_id = models.BigIntegerField(primary_key=True)
    city_id = models.BigIntegerField()
    district = models.CharField(max_length=500, blank=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'district_info'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class ImageInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    real_name = models.CharField(max_length=45, blank=True)
    random_name = models.CharField(max_length=45, blank=True)
    label = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=500, blank=True)
    thumbnail_url = models.CharField(max_length=45, blank=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    subtype = models.IntegerField(blank=True, null=True)
    pos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'image_info'


class ProductInfo(models.Model):
    product_id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    url = models.CharField(max_length=128, blank=True)
    product_name = models.CharField(max_length=255, blank=True)
    srv_sub_type = models.IntegerField(blank=True, null=True)
    product_type = models.IntegerField()
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    price = models.IntegerField()
    product_num = models.IntegerField()
    product_desc = models.CharField(max_length=255, blank=True)
    sales = models.IntegerField()
    evaluate = models.IntegerField()
    verify_status = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_info'


class SaleOrder(models.Model):
    order_id = models.CharField(primary_key=True, max_length=64)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    shop_id = models.IntegerField()
    product_num = models.IntegerField()
    money = models.IntegerField()
    begin_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    pay_type = models.IntegerField()
    is_coupon = models.IntegerField(blank=True, null=True)
    address_info = models.IntegerField()
    order_status = models.IntegerField()
    remark = models.CharField(max_length=256, blank=True)
    c_time = models.DateTimeField()
    m_time = models.DateTimeField()
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sale_order'


class SevicePeople(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    product_id = models.IntegerField()
    shop_id = models.IntegerField()
    phone = models.BigIntegerField()
    head_url = models.CharField(max_length=500, blank=True)
    hometown = models.CharField(max_length=128, blank=True)
    nick = models.CharField(max_length=500, blank=True)
    age = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=128, blank=True)
    work_years = models.IntegerField()
    introduction = models.CharField(max_length=500, blank=True)
    verify_status = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sevice_people'


class ShopInfo(models.Model):
    shop_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    shop_name = models.CharField(max_length=128, blank=True)
    shop_url = models.CharField(max_length=500, blank=True)
    type = models.IntegerField(blank=True, null=True)
    shoper = models.CharField(max_length=128, blank=True)
    shoper_phone = models.BigIntegerField(blank=True, null=True)
    telephone = models.BigIntegerField()
    srv_sub_type = models.CharField(max_length=128, blank=True)
    srv_community = models.CharField(max_length=128)
    shop_address = models.CharField(max_length=128, blank=True)
    post_address = models.CharField(max_length=128, blank=True)
    positive_idcard = models.CharField(max_length=128, blank=True)
    opposite_idcard = models.CharField(max_length=128, blank=True)
    hand_idcard = models.CharField(max_length=128, blank=True)
    business_license = models.CharField(max_length=256, blank=True)
    tax_license = models.CharField(max_length=256, blank=True)
    verify_status = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    srv_attitude = models.IntegerField(blank=True, null=True)
    srv_speed = models.IntegerField(blank=True, null=True)
    srv_contents = models.IntegerField(blank=True, null=True)
    order_num = models.IntegerField(blank=True, null=True)
    recommend = models.IntegerField(blank=True, null=True)
    entity = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    shop_desc = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'shop_info'


class SrvLimit(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    type = models.IntegerField(blank=True, null=True)
    requirement = models.CharField(max_length=256, blank=True)
    srv_limit = models.CharField(max_length=256, blank=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'srv_limit'


class UserComment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    product_id = models.IntegerField(blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=64)
    comment = models.CharField(max_length=500, blank=True)
    match_desc = models.IntegerField(blank=True, null=True)
    srv_attitude = models.IntegerField(blank=True, null=True)
    srv_speed = models.IntegerField(blank=True, null=True)
    srv_contents = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_comment'


class UserCoupon(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)
    sub_type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=256, blank=True)
    coupon_value = models.IntegerField()
    status = models.IntegerField()
    begin_time = models.IntegerField()
    end_time = models.IntegerField()
    order_id = models.CharField(max_length=64, blank=True)
    remark = models.CharField(max_length=256, blank=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    operator = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'user_coupon'


class UserFeedback(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    message = models.CharField(max_length=500, blank=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_feedback'


class UserInfo(models.Model):
    user_id = models.IntegerField(primary_key=True)
    phone = models.BigIntegerField(unique=True)
    head_url = models.CharField(max_length=500, blank=True)
    pwd = models.CharField(max_length=500, blank=True)
    nick = models.CharField(max_length=500, blank=True)
    sex = models.IntegerField(blank=True, null=True)
    address_id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    verify_status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'user_info'

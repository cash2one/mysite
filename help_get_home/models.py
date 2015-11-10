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


class ActivityInfo(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    position = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=128, blank=True)
    thumbnail = models.CharField(max_length=128, blank=True)
    detail_url = models.CharField(max_length=128, blank=True)
    detail_url_desc = models.CharField(max_length=128, blank=True)
    type = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_info'


class ActivityShop(models.Model):
    activity_id = models.IntegerField(primary_key=True)
    shop_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_shop'


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
    parent_id = models.BigIntegerField(blank=True, null=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_info'


class AtivityAd(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    image_id = models.IntegerField(blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=64, blank=True)
    sub_title = models.CharField(max_length=64, blank=True)
    image_url = models.CharField(max_length=128, blank=True)
    detail_url = models.CharField(max_length=45, blank=True)
    content = models.CharField(max_length=256, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    desc_url = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'ativity_ad'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(AuthUser, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CityInfo(models.Model):
    city_id = models.BigIntegerField(primary_key=True)
    city = models.CharField(max_length=500, blank=True)
    status = models.IntegerField()
    last_modify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_info'


class ClassifyInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=64, blank=True)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
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


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ImageInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    real_name = models.CharField(max_length=45, blank=True)
    random_name = models.CharField(max_length=45, blank=True)
    label = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=256, blank=True)
    thumbnail_url = models.CharField(max_length=256, blank=True)
    status = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    subtype = models.IntegerField(blank=True, null=True)
    pos = models.IntegerField()
    ref_id = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=45, blank=True)

    class Meta:
        managed = False
        db_table = 'image_info'


class ProductInfo(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=45, blank=True)
    shop_id = models.IntegerField()
    url = models.CharField(max_length=128, blank=True)
    thumbnail = models.CharField(max_length=128, blank=True)
    label = models.IntegerField()
    product_type = models.IntegerField()
    money = models.IntegerField()
    begin_time = models.CharField(max_length=32, blank=True)
    end_time = models.CharField(max_length=32, blank=True)
    price = models.IntegerField()
    product_num = models.IntegerField(blank=True, null=True)
    product_desc = models.CharField(max_length=4000, blank=True)
    sales = models.IntegerField()
    evaluate = models.IntegerField(blank=True, null=True)
    verify_status = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    last_modify = models.DateTimeField(blank=True, null=True)
    srv_sub_type = models.IntegerField()
    product_desc_url = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'product_info'


class ResourceInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=45)
    type = models.CharField(max_length=45, blank=True)
    url = models.CharField(max_length=64, blank=True)
    parent_id = models.IntegerField(blank=True, null=True)
    parent_ids = models.CharField(max_length=45, blank=True)
    code = models.CharField(max_length=32, blank=True)
    style = models.CharField(max_length=32, blank=True)
    permissions = models.CharField(max_length=128, blank=True)
    priority = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=64, blank=True)
    created_by = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resource_info'


class RoleInfo(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=32)
    resource_ids = models.CharField(max_length=500, blank=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role_info'


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
    user_id = models.IntegerField(blank=True, null=True)
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
    srv_type = models.IntegerField(blank=True, null=True)
    srv_sub_type = models.CharField(max_length=128, blank=True)
    srv_community = models.CharField(max_length=512)
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
    shop_desc = models.CharField(max_length=4000, blank=True)
    shop_desc_url = models.CharField(max_length=256, blank=True)

    class Meta:
        managed = False
        db_table = 'shop_info'


class ShopQuote(models.Model):
    id = models.BigIntegerField(primary_key=True)
    order_id = models.CharField(max_length=45, blank=True)
    product_id = models.CharField(max_length=32, blank=True)
    price = models.CharField(max_length=45, blank=True)
    mobile = models.CharField(max_length=45, blank=True)
    created = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True)
    remark = models.CharField(max_length=128, blank=True)

    class Meta:
        managed = False
        db_table = 'shop_quote'


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
    user_id = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    sub_type = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    desc_field = models.CharField(db_column='desc_', max_length=256, blank=True)  # Field renamed because it ended with '_'.
    coupon_value = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    begin_time = models.IntegerField(blank=True, null=True)
    end_time = models.IntegerField(blank=True, null=True)
    order_id = models.CharField(max_length=128, blank=True)
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
    address_id = models.IntegerField()
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    verify_status = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'


class UserRole(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user_id = models.IntegerField()
    role_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_role'

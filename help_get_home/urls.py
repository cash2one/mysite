from django.conf.urls import include,patterns, url
from rest_framework import routers
from help_get_home import views
router = routers.DefaultRouter()
router.register(r'userinfo', views.UserViewSet,"UserViewSet")
router.register(r'userinfo/(\d{0,9})/', views.UserViewSet.as_view({'get':'getuserinfo'}),"UserViewSet")
urlpatterns = patterns('',
            url(r'^index/$', views.index, name='index'),
            url(r'^getrollad/$',views.getrollad,name='getrollad'),
            url(r'^uploadimage/$',views.uploadimage,name='uploadimage'),
            url(r'^userfeedback/(\d{0,9})/(\d{1})/(\S{1,500})/$',views.userfeedback,name='userfeedback'),
            #url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/data/zhangchuhu/project/djproject/help_get_home/static/images/}'),
            url(r'^getsrvtype/(.+)/$',views.getsrvtype,name='getsrvtype'),
            url(r'^getareainfo/$',views.getareainfo,name='getareainfo'),
            url(r'^getcityinfo/$',views.getcityinfo,name='getcityinfo'),
            url(r'^getdistrictinfo/(.+)/$',views.getdistrictinfo,name='getdistrictinfo'),
            url(r'^updatemyaddress/$',views.updatemyaddress,name='updatemyaddress'),
            url(r'^addmyaddress/$',views.addmyaddress,name='addmyaddress'),
            url(r'^uploadheadimg/$',views.uploadheadimg,name='uploadheadimg'),
            url(r'^getmyaddrinfo/(.+)/$',views.getmyaddrinfo,name='getmyaddrinfo'),
            url(r'^getuserinfo/(.+)/$',views.getuserinfo,name='getuserinfo'),
            url(r'^login/$',views.login,name='login'),
            url(r'^register/$',views.register,name='register'),
            url(r'^unlicenseshoper/$',views.unlicenseshoper,name='unlicenseshoper'),
            url(r'^licenseshoper/$',views.licenseshoper,name='licenseshoper'),
            url(r'^checkisshoper/(.+)/$',views.checkisshoper,name='checkisshoper'),
            url(r'^srvlimit/(.+)/$',views.srvlimit,name='srvlimit'),
            url(r'^getshoperagreement/$',views.getshoperagreement,name='getshoperagreement'),
            url(r'^getverifycode/(\d*)/(\d*)/$',views.getverifycode,name='getverifycode'),
            url(r'^checkverifycode/(\d*)/(\d*)/(\d*)/$',views.checkverifycode,name='checkverifycode'),
            url(r'^getagreement/$',views.getagreement,name='getagreement'),
            url(r'^resetpwd/$',views.resetpwd,name='resetpwd'),
            url(r'^getshopinfo/(.+)/(.+)/(.+)/(.+)/$',views.getshopinfo,name='getshopinfo'),
            url(r'^getmyshop/(.+)/$',views.getmyshop,name='getmyshop'),
            url(r'^updatemyshopinfo/$',views.updatemyshopinfo,name='updatemyshopinfo'),
            url(r'^updateshopdesc/$',views.updateshopdesc,name='updateshopdesc'),
            url(r'^updateshopicon/$',views.updateshopicon,name='updateshopicon'),
            url(r'^getshopproduct/(.+)/(.+)/(.+)/(.+)/$',views.getshopproduct,name='getshopproduct'),
            url(r'^getproductbyshop/(.+)/(.+)/(.+)/$',views.getproductbyshop,name='getproductbyshop'),
            url(r'^getproductbyid/(.+)/$',views.getproductbyid,name='getproductbyid'),
            url(r'^addorder/$',views.addorder,name='addorder'),
            url(r'^addshoppingcart/$',views.addshoppingcart,name='addshoppingcart'),
            url(r'^getmyorder/(.+)/(.+)/$',views.getmyorder,name='getmyorder'),
            url(r'^orderquery/(.+)/$',views.orderquery,name='orderquery'),
            url(r'^getpayreq/(.+)/$',views.getpayreq,name='getprepay'),
            url(r'^getshoperorder/(.+)/(.+)/$',views.getshoperorder,name='getshoperorder'),
            url(r'^updateorderstatus/$',views.updateorderstatus,name='updateorderstatus'),
            url(r'^updateshoppingcart/$',views.updateshoppingcart,name='updateshoppingcart'),
            url(r'^login/(.+)/(.+)/$',views.login,name='login'),
            url(r'^addusercomment/$',views.addusercomment,name='addusercomment'),
            url(r'^getusercomment/(.+)/$',views.getusercomment,name='getusercomment'),
            url(r'^createtoken/(.+)/$',views.createtoken,name='createtoken'),
            url(r'^getad/(.+)/$',views.getad,name='getad'),
            url(r'^getdetailad/(.+)/$',views.getdetailad,name='getdetailad'),
            url(r'^', include(router.urls)),

            )

from django.urls import path, re_path
from . import views
from django.contrib.auth.views import login, logout

app_name = 'BuyMed'
urlpatterns=[
	# re_path(r'^$', views.product_list, name='product_list'),
        re_path(r'^product/$', views.product_list, name='product_list'),
        re_path(r'^(?P<category_slug>[-\w]+)/$',
                views.product_list,
                name='product_list_by_category'),
        re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
                views.product_detail,
                name='product_detail'),
        re_path(r'^product/search/$', 
                views.product_name_search,
                name='product_name_search'),
        re_path(r'^product/search/([a-zA-Z]+)/$',
                views.product_name_search,
                name="product_name_search"),
        re_path(r'^product/login/$', login),
        re_path(r'^product/logout/$', logout),
]
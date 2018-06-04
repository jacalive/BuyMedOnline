from django.urls import path, re_path
from . import views

app_name = 'checkout'
urlpatterns = [
    re_path(r'^$', views.checkout_detail, name='checkout_detail'),
    re_path(r'^remove/(?P<product_id>\d+)/$',
            views.checkout_remove,
            name='checkout_remove'),
]

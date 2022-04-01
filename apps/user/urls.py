from django.urls import path
from rest_framework import routers
from apps.user.admin import enable_disable_captcha

app_name = 'user'

router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path('enable-disable-captcha/', enable_disable_captcha, name='enable_disable_captcha')
]

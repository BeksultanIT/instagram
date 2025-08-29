from django.urls import path, include
from rest_framework import routers

from api_v1.views import PostViewSet

app_name = 'v1'

router = routers.DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
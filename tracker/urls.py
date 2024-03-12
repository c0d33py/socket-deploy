from django.urls import include, path
from rest_framework import routers

from .views import IndexTemplateRender, YoutubeFilterTrackerViewSetAPI

router = routers.DefaultRouter()
router.register(r'tracker', YoutubeFilterTrackerViewSetAPI, basename='tracker')

urlpatterns = [
    path('', IndexTemplateRender.as_view(), name='home_page'),
    path('api/', include(router.urls)),
]

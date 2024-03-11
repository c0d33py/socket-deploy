from django.urls import path

from .views import IndexTemplateRender, YoutubeFilterTrackerViewSetAPI

urlpatterns = [
    path('', IndexTemplateRender.as_view(), name='home_page'),
    path(
        'api/',
        YoutubeFilterTrackerViewSetAPI.as_view({'get': 'list', 'post': 'create'}),
    ),
]

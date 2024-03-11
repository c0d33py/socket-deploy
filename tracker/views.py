from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import YoutubeFilterTracker
from .serializers import YoutubeFilterTrackerSerializer


class IndexTemplateRender(TemplateView):
    template_name = 'index.html'


class YoutubeFilterTrackerViewSetAPI(ModelViewSet):
    """
    Youtube filter tracker viewset API.
    """

    serializer_class = YoutubeFilterTrackerSerializer
    queryset = YoutubeFilterTracker.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'privacy_level']
    search_fields = ['title']

    @action(detail=True, methods=['get'])
    def share(self, request, pk=None):
        obj = self.get_object()
        obj.share_count += 1
        obj.save()
        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(obj).data,
        )

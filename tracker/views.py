from django.views.generic import TemplateView
from rest_framework import filters, pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import YoutubeFilterTrackerForm
from .models import YoutubeFilterTracker
from .serializers import YoutubeFilterTrackerSerializer
from .tasks import channel_statistics_api_task


class IndexTemplateRender(TemplateView):
    """
    Index template view.
    """

    template_name = 'index.html'
    form_class = YoutubeFilterTrackerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context


class YoutubeFilterTrackerViewSetAPI(ModelViewSet):
    """
    Youtube filter tracker viewset API.
    """

    serializer_class = YoutubeFilterTrackerSerializer
    queryset = YoutubeFilterTracker.objects.filter(privacy_level='Private')
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter]
    pagination_class.page_size = 10
    search_fields = ['title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        obj = serializer.save(created_by=user)

        _ids = [
            # Generate unique random strings
            'leEw3z',
            '7eEw3z',
            'weL33z',
            'wRe23z',
            'wRe43z',
        ]

        task = channel_statistics_api_task.delay(
            **{
                'instance': obj.id,
                'channel_ids': _ids,
                'start_date': obj.start_date,
                'end_date': obj.end_date,
                'user_id': user.id,
            }
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'task_id': task.id,
                'data': serializer.data,
            },
        )

    @action(detail=False, methods=["get"], url_path=r'public')
    def public(self, request, pk=None):
        queryset = YoutubeFilterTracker.objects.filter(privacy_level='Public')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    @action(detail=True, methods=["get"], url_path=r'share')
    def share(self, request, pk=None):
        obj = self.get_object()
        obj.share_count += 1
        obj.save()
        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(obj).data,
        )

    @action(detail=True, methods=["get"], url_path=r'rating')
    def rating(self, request, pk=None):
        obj = self.get_object()
        obj.rating += 1
        obj.save()
        return Response(
            status=status.HTTP_200_OK,
            data=self.get_serializer(obj).data,
        )

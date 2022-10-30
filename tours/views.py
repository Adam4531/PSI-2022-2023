from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response

from tours.models import TypeOfTour, Tour


class TourCategoryList(generics.ListCreateAPIView):
    queryset = TypeOfTour.objects.all()
    name = 'types_of_tour'
    filterset_fields = ['name_of_type']
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']


class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    name = 'tour-list'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'tour-categories': reverse(TourCategoryList.name, request=request),
                         'tours': reverse(TourList.name, request=request)
                         })

from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.response import Response

from tours.models import TypeOfTour, Tour, Price, User, Places
from tours.serializers import TypeOfTourSerializer, TourSerializer, PriceSerializer, UserSerializer, PlacesSerializer


class TourCategoryList(generics.ListCreateAPIView):
    queryset = TypeOfTour.objects.all() #FIXME change db table, row names and django names to universal i.e.: Django: TourCategory; db:TourCategories
    serializer_class = TypeOfTourSerializer
    name = 'type_of_tour'
    filterset_fields = ['name_of_type']
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']


class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    name = 'tour-list'


class PriceDetail(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    name = 'price'

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user'

class PlacesList(generics.ListCreateAPIView):
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    name = 'places'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'tour-categories': reverse(TourCategoryList.name, request=request),
                         'tours': reverse(TourList.name, request=request),
                         'price': reverse(PriceDetail.name, request=request),
                         'user': reverse(UserList.name, request=request),
                         'places': reverse(PlacesList.name, request=request)
                         })

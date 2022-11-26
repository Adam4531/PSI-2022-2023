from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tours.models import TourCategory, Tour, Price, User, Place
from tours.serializers import TourCategorySerializer, TourSerializer, PriceSerializer, UserSerializer, PlaceSerializer


class TourCategoryList(generics.ListCreateAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    name = 'tour-categories'
    filterset_fields = ['name_of_type']
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']


class TourCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    name = 'tourcategory-detail'


class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    name = 'tour-list'


class TourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    name = 'tour-detail'


class PriceList(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    name = 'price-list'


class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    name = 'price-detail'


class UserList(generics.ListCreateAPIView):
    # permission_classes = [isAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    name = 'places'


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    name = 'place-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'tour-categories': reverse(TourCategoryList.name, request=request),
                         # 'tourcategory-detail': reverse(TourCategoryDetail.name, request=request),
                         'tours': reverse(TourList.name, request=request),
                         'prices': reverse(PriceList.name, request=request),
                         'users': reverse(UserList.name, request=request),
                         'places': reverse(PlaceList.name, request=request)
                         })

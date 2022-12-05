from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions as base_permissions

from tours import custompagination, custompermissions
from tours.models import TourCategory, Tour, Price, User, Place, Reservation
from tours.serializers import TourCategorySerializer, TourSerializer, PriceSerializer, UserSerializer, PlaceSerializer, \
    ReservationSerializer


# TODO make serializers great again, without copies

class TourCategoryList(generics.ListCreateAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tour-categories'
    filterset_fields = ['name_of_type']
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']

    # def view_index(self, name):
    #     queryset = TourCategory.objects.filter('')


# class createTourCategory(generics.CreateAPIView):

#     queryset = TourCategory.objects.all()
#     serializer_class = TourCategorySerializer
#     name = 'tour-category-detail'


class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tour-list'

#
# class getTourByTourCategory(generics.ListAPIView):
#     context_object_name = ''
#     queryset = Tour
#     name = 'tour-detail'

class TourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    name = 'tour-detail'


class PriceList(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'price-list'


# class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Price.objects.all()
#     serializer_class = PriceSerializer
#     name = 'price-detail'


class UserList(generics.ListCreateAPIView):
    # permission_classes = [base_permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'user'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [base_permissions.IsAuthenticatedOrReadOnly,
                          custompermissions.isOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'places'


# class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Place.objects.all()
#     serializer_class = PlaceSerializer
#     name = 'place-detail'


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'reservations'

class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    name = 'reservation-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'tour-categories': reverse(TourCategoryList.name, request=request),
                         # 'tourcategory-detail': reverse(TourCategoryDetail.name, request=request),
                         'tours': reverse(TourList.name, request=request),
                         'prices': reverse(PriceList.name, request=request),
                         'users': reverse(UserList.name, request=request),
                         'places': reverse(PlaceList.name, request=request),
                         'reservations': reverse(ReservationList.name, request=request)
                         })

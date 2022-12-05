from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions as base_permissions
from django_filters import FilterSet

from tours import custompagination
from tours.models import TourCategory, Tour, Price, User, Place, Reservation
from tours.serializers import TourCategorySerializer, TourSerializer, PriceSerializer, UserSerializer, PlaceSerializer, \
    ReservationSerializer


# TODO make serializers great again, without copies

class TourCategoryList(generics.ListCreateAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tourcategory-list'
    filterset_fields = ['name_of_type']
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']


class TourCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TourCategory.objects.all()
    serializer_class = TourCategorySerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tourcategory-detail'


class TourList(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tour-list'
    # filterset_fields = ['']
    # filter_class = Filter
    # search_fields = ['']
    # ordering_fields = ['']

    # class TourFilter(FilterSet):


        # class Meta:



class TourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'tour-detail'


class PriceList(generics.ListCreateAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'price-list'
    # filterset_fields = ['']
    # search_fields = ['']
    # ordering_fields = ['']


class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'price-detail'
    # filter_class = PriceFilter


# class PriceFilter(FilterSet):
#
#
#     class Meta:


class UserList(generics.ListCreateAPIView):
    permission_classes = [base_permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'user-list'
    filterset_fields = ['email', 'first_name', 'last_name']
    search_fields = ['email']
    ordering_fields = ['last_name', 'first_name', 'email']


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    #     permission_classes = [base_permissions.IsAuthenticatedOrReadOnly,
    #                           custompermissions.isOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'user-detail'


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'place-list'
    # filterset_fields = ['']
    # search_fields = ['']
    # ordering_fields = ['']


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'place-detail'


class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'reservation-list'
    # filterset_fields = ['']
    # search_fields = ['']
    # ordering_fields = ['']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'reservation-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'tour-categories': reverse(TourCategoryList.name, request=request),
                         'tours': reverse(TourList.name, request=request),
                         'prices': reverse(PriceList.name, request=request),
                         'users': reverse(UserList.name, request=request),
                         'places': reverse(PlaceList.name, request=request),
                         'reservations': reverse(ReservationList.name, request=request)
                         })

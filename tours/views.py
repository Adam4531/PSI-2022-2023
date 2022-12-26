from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tours import custompagination
from tours.models import TourCategory, Tour, Price, User, Place, Reservation
from tours.serializers import TourCategorySerializer, TourSerializer, PriceSerializer, UserSerializer, PlaceSerializer,\
    ReservationSerializer


# TODO check if copies are possible

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
    filterset_fields = ['date_start', 'date_end', 'price', 'type_of_tour', 'place', 'unit_price']
    # filter_class = TourFilter
    search_fields = ['date_start', 'date_end', 'price', 'type_of_tour', 'place', 'unit_price']
    ordering_fields = ['type_of_tour', 'place', 'date_start', 'price']

    # def get(self, request):
    #     tours = Tour.objects.all()
    #     serializer = TourSerializer(tours, many=True, context={'request':request})
    #     return Response(serializer.data)


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
    search_fields = ['normal_price']
    ordering_fields = ['normal_price']


class PriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = custompagination.LimitOffsetPaginationWithUpperBound
    name = 'price-detail'


# class PriceFilter(FilterSet):
#
#
#     class Meta:


class UserList(generics.ListCreateAPIView):
    # permission_classes = [base_permissions.IsAuthenticatedOrReadOnly]
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
    filterset_fields = ['destination', 'country', 'accommodation']
    search_fields = ['destination', 'country', 'accommodation']
    ordering_fields = ['destination', 'country', 'accomomdation']


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
    filterset_fields = ['dateOfReservation', 'tour', 'total_price', 'amount_of_adults', 'amount_of_children']
    search_fields = ['tour', 'total_price', 'dateOfReservation']
    ordering_fields = ['dateOfReservation', 'tour', 'amount_of_adults', 'total_price']

    # def perform_create(self, serializer):

    #     serializer.save(user=self.request.user)

    # def change_total_price(self):
    #     self.total_price = self.amount_of_adults* self.tour.+ self.amount_of_children * self.reduced_price


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

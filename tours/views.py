from rest_framework import generics

from TravelAgency.Tours.models import TypeOfTour


class TourCategoryList(generics.ListCreateAPIView):
    queryset = TypeOfTour.objects.all()
    name = 'types_of_tour'
    filterset_fields = ['name_of_type'] #FIXME or just 'name'
    search_fields = ['name_of_type']
    ordering_fields = ['name_of_type']

    

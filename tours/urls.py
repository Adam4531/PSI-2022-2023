from django.urls import path
from tours import views

urlpatterns = [
    path('tour-categories', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tour-categories/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tours', views.TourList.as_view(), name=views.TourList.name),
    path('tours/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('price', views.PriceList.as_view(), name=views.PriceList.name),
    path('price/<int:pk>', views.PriceList.as_view(), name=views.PriceList.name),
    path('user', views.UserList.as_view(), name=views.UserList.name),
    path('user/<int:pk>', views.UserList.as_view(), name=views.UserList.name),
    path('places', views.PlaceList.as_view(), name=views.PlaceList.name),
    path('places/<int:pk>', views.PlaceList.as_view(), name=views.PlaceList.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
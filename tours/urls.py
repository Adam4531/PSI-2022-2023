from django.urls import path
from tours import views

urlpatterns = [
    path('tour-categories', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tour-categories/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tours', views.TourList.as_view(), name=views.TourList.name),
    path('tours/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('price', views.PriceDetail.as_view(), name=views.PriceDetail.name),
    path('price/<int:pk>', views.PriceDetail.as_view(), name=views.PriceDetail.name),
    path('user', views.UserList.as_view(), name=views.UserList.name),
    path('user/<int:pk>', views.UserList.as_view(), name=views.UserList.name),
    path('places', views.PlacesList.as_view(), name=views.PlacesList.name),
    path('places/<int:pk>', views.PlacesList.as_view(), name=views.PlacesList.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
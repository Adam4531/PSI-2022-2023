from django.urls import path
from tours import views

urlpatterns = [
    path('tour-categories', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    # path('tour-categories/<int:pk>/', views.TourCategoryDetail.as_view(), name=views.TourCategoryDetail.name),
    path('tours', views.TourList.as_view(), name=views.TourList.name),
    path('tours/<int:pk>/', views.TourDetail.as_view(), name=views.TourDetail.name),
    path('price', views.PriceList.as_view(), name=views.PriceList.name),
    # path('price/<int:pk>/', views.PriceDetail.as_view(), name=views.PriceDetail.name),
    path('user', views.UserList.as_view(), name=views.UserList.name),
    path('user/<int:pk>/', views.UserDetail.as_view(), name=views.UserDetail.name),
    path('places', views.PlaceList.as_view(), name=views.PlaceList.name),
    # path('places/<int:pk>/', views.PlaceDetail.as_view(), name=views.PlaceDetail.name),
    path('reservations', views.ReservationList.as_view(), name=views.ReservationList.name),
    path('reservations/<int:pk>/', views.ReservationDetail.as_view(), name=views.ReservationDetail.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
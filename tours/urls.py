from django.urls import path
from tours import views

urlpatterns = [
    path('tour-categories', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tour-categories/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('tours', views.TourList.as_view(), name=views.TourList.name),
    path('tours/<int:pk>', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
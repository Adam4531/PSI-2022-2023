from django.urls import path
from Tours import views

urlpatterns = [
    path('types-of-tour', views.TourCategoryList.as_view(), name=views.TourCategoryList.name),

]
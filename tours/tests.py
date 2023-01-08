from django import urls
from django.test import TestCase
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from . import views
from .models import TourCategory


class TourCategoryTests(APITestCase):
    def post_tour_category(self, name):
        url = reverse(views.TourCategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_tour_category(self):
        new_tour_category_name = "all-inclusive"
        response = self.post_tour_category(new_tour_category_name)
        print("PK {0}".format(TourCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert TourCategory.objects.count() == 1
        assert TourCategory.objects.get().name == new_tour_category_name

    def test_post_existing_tour_category_name(self):
        url = reverse(views.TourCategoryList.name)
        new_tour_category_name = 'Duplicate all-inclusive'
        data = {'name': new_tour_category_name}
        reponse_one = self.post_tour_category(new_tour_category_name)
        assert reponse_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_tour_category(new_tour_category_name)
        print(response_two)
        assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_tour_category_by_name(self):
        tour_category_name_one = 'all-inclusive'
        tour_category_name_two = 'poor'
        self.post_tour_category(tour_category_name_one)
        self.post_tour_category(tour_category_name_two)
        filter_by_name = {'name': tour_category_name_one}
        url = '{0}?{1}'.format(reverse(views.TourCategoryList.name), urlencode(filter_by_name))
        print(url)
        reponse = self.client.get(url, format='json')
        assert reponse.status_code == status.HTTP_200_OK
        assert reponse.data['count'] == 2
        assert reponse.data['results'][0]['name'] == tour_category_name_one

    def test_get_tour_categories_collection(self):
        new_tour_category_name = 'standard'
        self.post_tour_category(new_tour_category_name)
        url = reverse(views.TourCategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_tour_category_name

    def test_update_tour_category(self):
        tour_category_name = 'standard'
        response = self.post_tour_category(tour_category_name)
        url = urls.reverse(views.TourCategoryDetail.name, None, [response.data['pk']])
        updated_tour_category_name = 'new standard'
        data = {'name': updated_tour_category_name}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_tour_category_name

    def test_get_tour_category(self):
        tour_category_name = 'standard'
        response = self.post_tour_category(tour_category_name)
        url = urls.reverse(views.TourCategoryDetail.name, None, [response.data['pk']])
        get_response = self.client.patch(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == tour_category_name



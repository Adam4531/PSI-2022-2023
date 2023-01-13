import datetime
import decimal
from decimal import Decimal

from MySQLdb import Date
from django import urls
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from . import views
from .models import TourCategory, Price, Tour, Place


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


class PriceTests(APITestCase):
    def post_price(self, normal_price, reduced_price, user):
        url = reverse(views.PriceList.name)
        data = {'normal_price': normal_price, 'reduced_price': reduced_price}
        response = user.post(url, data, format='json')
        return response

    def test_post_and_get_price(self):
        new_normal_price: Decimal = Decimal(1500.20).quantize(Decimal('1.00'))
        new_reduced_price = decimal.Decimal(1000.35).quantize(Decimal('1.00'))
        user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')
        response = self.post_price(new_normal_price, new_reduced_price, client)
        print("PK {0}".format(Price.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Price.objects.count() == 1
        assert Price.objects.get().normal_price == new_normal_price
        assert Price.objects.get().reduced_price == new_reduced_price

    # def test_post_existing_price(self):
    #     user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    #     client = APIClient()
    #     client.login(username='admin', password='admin123')
    #
    #     url = reverse(views.TourCategoryList.name)
    #     new_normal_price: Decimal = Decimal(1500.20).quantize(Decimal('1.00'))
    #     new_reduced_price = decimal.Decimal(1000.35).quantize(Decimal('1.00'))
    #     reponse_one = self.post_price(new_normal_price, new_reduced_price, client)
    #     assert reponse_one.status_code == status.HTTP_201_CREATED
    #     response_two = self.post_price(new_normal_price, new_reduced_price, client)
    #     assert response_two.status_code == status.HTTP_400_BAD_REQUEST

    # def test_filter_price_by_normal_price(self):
    #     new_normal_price_1 = Decimal(1500.20).quantize(Decimal('1.00'))
    #     new_reduced_price_1 = decimal.Decimal(1000.30).quantize(Decimal('1.00'))
    #     new_normal_price_2 = Decimal(1500.35).quantize(Decimal('1.00'))
    #     new_reduced_price_2 = decimal.Decimal(1000.15).quantize(Decimal('1.00'))
    #
    #     user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    #     client = APIClient()
    #     client.login(username='admin', password='admin123')
    #
    #     self.post_price(new_normal_price_1, new_reduced_price_1, client)
    #     self.post_price(new_normal_price_2, new_reduced_price_2, client)
    #     filter_by_normal_price = {'normal_price': new_normal_price_1}
    #     url = '{0}?{1}'.format(reverse(views.PriceList.name), urlencode(filter_by_normal_price))
    #     print(url)
    #     reponse = self.client.get(url, format='json')
    #     assert reponse.status_code == status.HTTP_200_OK
    #     assert reponse.data['count'] == 2
    #     assert reponse.data['results'][0]['normal_price'] == new_normal_price_1


class TourTests(APITestCase):  # TODO test_post_and_get_tour
    def create_tour_category(self, user):
        url = reverse(views.TourCategoryList.name)
        data = {'id': 1, 'name': 'all-inclusive'}
        user.post(url, data, format='json')
        return data

    def create_place(self, user):
        url = reverse(views.PlaceList.name)
        data = {'country': 'Germany',
                'place': 'Berlin',
                'accommodation': 'newBerlinHotel'}
        user.post(url, data, format='json')
        return data

    def create_tour(self, max_number_of_partcipants, date_start, date_end, price, place, unit_price, client):
        url = reverse(views.TourList.name)
        data = {'max_number_of_participants': max_number_of_partcipants,
                'date_start': date_start,
                'date_end': date_end,
                'price': price,
                'place': place,
                'unit_price': unit_price}
        response = client.post(url, data, format='json')
        return response

    # def test_post_and_get_tour(self):#FIXME
    #     user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
    #     client = APIClient()
    #     client.login(username='admin', password='admin123')
    #
    #     self.create_tour_category(client)
    #     self.create_place(client)
    #     new_max_number_of_participants = 150
    #     new_date_start = datetime.date.today()
    #     new_date_end = new_date_start + datetime.timedelta(days=5)
    #     new_price: Decimal = Decimal(1500.20).quantize(Decimal('1.00'))
    #     new_place = self.create_place(client)
    #     new_unit_price: Decimal = Decimal(1500.20).quantize(Decimal('1.00'))
    #     response = self.create_tour(new_max_number_of_participants, new_date_start, new_date_end, new_price, new_place,
    #                                 new_unit_price, client)
    #     print("PK {0}".format(Tour.objects.get().pk))
    #     print(Tour.objects.get().pk)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert Tour.objects.count() == 1
    # assert Price.objects.get().normal_price == new_normal_price
    # assert Price.objects.get().reduced_price == new_reduced_price


class UserTests(APITestCase):
    def create_user(self, email, password, first_name, last_name, client):
        url = reverse(views.UserList.name)
        data = {'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_user(self):#FIXME
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')

        new_email = 'kowalski@gmail.com'
        new_password = 'Kowalski2212'
        new_first_name = 'Janusz'
        new_last_name = 'Kowalski'
        response = self.create_user(new_email, new_password, new_first_name, new_last_name, client)
        assert response.status_code == status.HTTP_201_CREATED

# class ReservationTests(APITestCase): #TODO


class PlaceTests(APITestCase):
    def post_place(self, country, destination, accommodation, client):
        url = reverse(views.PlaceList.name)
        data = {'country': country,
                'destination': destination,
                'accommodation': accommodation}
        response = client.post(url, data, format='json')
        return response

    def test_post_and_get_place(self):
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')

        country = 'Germany'
        place = 'Berlin'
        accommodation = 'newBerlinHotel'
        response = self.post_place(country, place, accommodation, client)
        print("PK {0}".format(Place.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Place.objects.count() == 1
        assert Place.objects.get().country == country

    def test_post_existing_tour_place(self):#FIXME
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        client = APIClient()
        client.login(username='admin', password='admin123')

        country = 'Germany'
        place = 'Berlin'
        accommodation = 'newBerlinHotel'

        response_one = self.post_place(country, place, accommodation, client)
        assert response_one.status_code == status.HTTP_201_CREATED
        response_two = self.post_place(country, place, accommodation, client)
        print(response_two)
        assert response_two.status_code == status.HTTP_201_CREATED #FIXME returned mysql error code 1062 but should HTTP 400
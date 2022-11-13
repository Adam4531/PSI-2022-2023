from rest_framework import serializers
import pycountry
import datetime
from email_validator import validate_email, EmailNotValidError

from tours import models
from tours.models import TypeOfTour, Places, Price, User


class TypeOfTourSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=45, unique=True)


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    normal_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    reduced_price = serializers.DecimalField(max_digits=7, decimal_places=2)

    def validate_reduced_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        return value

    def validate_normal_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        return value


class PlacesSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.CharField(max_length=45)
    place = serializers.CharField(max_length=45)
    accommodation = serializers.CharField(max_length=45)

    def validate_country(self, value):
        if value not in pycountry.countries.name:
            raise serializers.ValidationError(
                "Country does not exist",
            )
        return value


class TourSerializer(serializers.HyperlinkedModelSerializer):
    max_number_of_participants = serializers.IntegerField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    type_of_tour = serializers.ForeignKey(TypeOfTour, related_name='type_of_tour', on_delete=models.CASCADE)
    place = serializers.ForeignKey(Places, related_name='places', on_delete=models.CASCADE)
    unit_price = serializers.ForeignKey(Price, related_name='price', on_delete=models.CASCADE)

    def validate_max_number_of_participants(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make number of participants lower or equal to zero", )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        return value

    def validate_date_start(self, value):
        if value < datetime.date:
            raise serializers.ValidationError("Start cannot be in the past", )
        return value

    def validate_date_end(self, value):
        if value > self.date_start:
            raise serializers.ValidationError("End cannot be before start", )
        return value


class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.CharField(max_length=30, unique=True)
    password = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)

    def validate_email(self, value):
        try:
            # validate and get info
            v = validate_email(value)
            # replace with normalized form
            email = v["email"]
            return value
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            raise serializers.ValidationError(print(str(e)), )

        def validate_first_name(self, value):
            value = value.title()
            return value

        def validate_last_name(self, value):
            value = value.title()
            return value

        def validate_password(self, value):
            if len(value) > 8:
                if [A - Z] in value:  # FIXME Unresolved reference 'A' and 'Z'
                    if [0 - 9] in value:
                        return value
                    else:
                        raise serializers.ValidationError("Password need to have number", )
                else:
                    raise serializers.ValidationError("Password need to have big letter", )
            else:
                raise serializers.ValidationError("Short password", )


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    date = serializers.DateField
    amount_of_adults = serializers.IntegerField()
    amount_of_children = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    tour = serializers.IntegerField()

    def validate_amount_of_adults(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make number of adults lower or equal to zero", )
        return value

    def validate_amount_of_children(self, value):
        if value < 0:
            raise serializers.ValidationError("Don't make number of childrens lower to zero", )
        return value

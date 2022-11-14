import datetime

import pycountry
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers

from tours.models import TypeOfTour, Tour


class TypeOfTourSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=45, )

    class Meta:
        model = TypeOfTour
        fields = ['name']


class PriceSerializer(serializers.ModelSerializer): #TODO
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


class PlacesSerializer(serializers.ModelSerializer): #TODO
    country = serializers.CharField(max_length=45)
    place = serializers.CharField(max_length=45)
    accommodation = serializers.CharField(max_length=45)

    def validate_country(self, value):
        if value not in pycountry.countries.name:
            raise serializers.ValidationError(
                "Country does not exist",
            )
        return value


class TourSerializer(serializers.ModelSerializer):
    max_number_of_participants = serializers.IntegerField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    # type_of_tour = serializers.ForeignKey(TypeOfTour, related_name='type_of_tour', on_delete=models.CASCADE)
    type_of_tour = TypeOfTourSerializer(many=False, read_only=True)
    place = PlacesSerializer(many=True, read_only=True)
    unit_price = PriceSerializer(many=False, read_only=True)

    class Meta:
        model = Tour
        fields = ['id','max_number_of_participants','date_start','date_end','price','place','type_of_tour','unit_price']


    def validate_max_number_of_participants(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make number of participants lower or equal to zero", )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        return value

    def validate_date_start(self, value):
        if value > self.date_end:
            raise serializers.ValidationError("Start cannot be in the past", )
        return value

    def validate_date_end(self, value):
        if value > self.date_start:
            raise serializers.ValidationError("End cannot be before start", )
        return value


class UserSerializer(serializers.ModelSerializer): #TODO
    email = serializers.CharField(max_length=30)
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
                for el in value:
                    if el.isupper():  # FIXME Unresolved reference 'A' and 'Z'
                        if el.isdigit():
                            return value
                        else:
                            raise serializers.ValidationError("Password need to have number", )
                    else:
                        raise serializers.ValidationError("Password need to have big letter", )
            else:
                raise serializers.ValidationError("Short password", )


class ReservationSerializer(serializers.ModelSerializer): #TODO
    user = UserSerializer(many=True, read_only=True)
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

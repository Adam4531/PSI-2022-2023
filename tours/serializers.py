import pycountry
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers

from tours.models import TypeOfTour, Tour, Price, Places, User, Reservation


# TODO read about types of serializers.Slugfield/HyperLink and how to use it

class TypeOfTourSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=45, )

    class Meta:
        model = TypeOfTour
        fields = ['name']


class PriceSerializer(serializers.ModelSerializer):
    normal_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    reduced_price = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        model = Price
        fields = ['normal_price', 'reduced_price']

    def validate_reduced_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        if value > 99999:
            raise serializers.ValidationError("Reduced price can not be higher than 99 999", )
        return value

    def validate_normal_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero", )
        if value > 99999:
            raise serializers.ValidationError("Normal price can not be higher than 99 999", )
        return value

    def validate_reduced_price_compared_to_normal_price(self, reduced, normal):
        if reduced > normal:
            raise serializers.ValidationError("Reduced price can not be higher than normal price!", )
        return reduced


class PlacesSerializer(serializers.ModelSerializer):  # TODO
    country = serializers.CharField(max_length=45)
    place = serializers.CharField(max_length=45)
    accommodation = serializers.CharField(max_length=45)

    class Meta:
        model = Places
        fields = ['country', 'place', 'accommodation']

    def validate_country(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Country field can not be empty!", )
        if len(value) > 45:
            raise serializers.ValidationError("Country field can have only 45 characters!", )
        if value not in pycountry.countries.name:
            raise serializers.ValidationError(
                "Country does not exist",
            )
        return value

    def validate_place(self, value):
        if len(value) > 45:
            raise serializers.ValidationError("Place field can have only 45 characters!", )
        if len(value) == 0:
            raise serializers.ValidationError("Place field can not be empty!", )
        return value

    def validate_accommodation(self, value):
        if len(value) > 45:
            raise serializers.ValidationError("Accommodation field can have only 45 characters!", )
        if len(value) == 0:
            raise serializers.ValidationError("Accommodation field can not be empty!", )
        return value


class TourSerializer(serializers.ModelSerializer):  # TODO
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
        fields = ['max_number_of_participants', 'date_start', 'date_end', 'price', 'place', 'type_of_tour',
                  'unit_price']

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
            raise serializers.ValidationError("Start date cannot be in the past", )
        return value

    def validate_date_end(self, value):
        if value > self.date_start:
            raise serializers.ValidationError("End date cannot be before start date", )
        return value


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

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
        if len(value) == 0:
            raise serializers.ValidationError("First name field can not be empty!", )
        if len(value) > 45:
            raise serializers.ValidationError("First name can not be longer than 45 characters!", )
        if value.islower():
            raise serializers.ValidationError("First name should start from Uppercase!", )
        return value

    def validate_last_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Last name field can not be empty!", )
        if len(value) > 45:
            raise serializers.ValidationError("Last name can not be longer than 45 characters!", )
        if value.islower():
            raise serializers.ValidationError("Last name should start from Uppercase!", )
        return value

    def validate_password(self, value):
        if len(value) > 8:
            for el in value:
                if el.isupper():
                    if el.isdigit():
                        return value
                    else:
                        raise serializers.ValidationError("Password need to have at least one number", )
                else:
                    raise serializers.ValidationError("Password need to have at least one big letter", )
        else:
            raise serializers.ValidationError("Short have to contain at least 8 characters", )


class ReservationSerializer(serializers.ModelSerializer):  # TODO
    user = UserSerializer(many=True, read_only=True)
    date = serializers.DateField
    amount_of_adults = serializers.IntegerField()
    amount_of_children = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    tour = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = ['user', 'date', 'amount_of_adults', 'amount_of_children', 'total_price', 'tour']

    def validate_amount_of_adults(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of the adults must be higher than 0!", )
        return value

    def validate_amount_of_children(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of the children can not be lower than zero!", )
        return value

    def validate_date(self, value):  # TODO how to validate this date? "reservationDate < now" does not have any sense
        # now = datetime.now()
        if len(value) == 0:
            raise serializers.ValidationError("Date field can not be empty!", )
        return value

    def validate_total_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Total price can not be lower than zero!", )
        if value > 99999:
            raise serializers.ValidationError("Total price can not be higher than 99 999", )

        return value

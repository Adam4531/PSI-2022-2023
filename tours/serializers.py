import pycountry
from iso3166 import countries
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers

from tours.models import TourCategory, Tour, Price, Place, User, Reservation


class TourCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    name = serializers.CharField(max_length=45, )

    class Meta:
        model = TourCategory
        fields = ['id','name']


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


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    country = serializers.CharField(max_length=45,)
    destination = serializers.CharField(max_length=45,)
    accommodation = serializers.CharField(max_length=45,)

    class Meta:
        model = Place
        fields = ['id','country', 'destination', 'accommodation']

    def validate_country(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Country field can not be empty!", )
        if len(value) > 45:
            raise serializers.ValidationError("Country field can have only 45 characters!", )
        if value not in countries:
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


#FIXME Cannot assign "OrderedDict([('country', 'Poland'), ('place', 'Warsaw'), ('accommodation', 'Stoleczna 44')])":
# "Tour.place" must be a "Places" instance.
# to resolve problem you have to add view to it, i.e.:
# Change view code, assign User object instead.
#
# author = User.objects.get(username=request.POST["username"])

class TourSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    max_number_of_participants = serializers.IntegerField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    price = serializers.DecimalField(max_digits=7, decimal_places=2) #TODO do we need that?
    type_of_tour = TourCategorySerializer(many=False,).data
    place = PlaceSerializer(many=False, ).data
    unit_price = PriceSerializer(many=False, ).data

    class Meta:
        model = Tour
        fields = ['id', 'max_number_of_participants', 'date_start', 'date_end', 'price', 'place', 'type_of_tour',
                  'unit_price']

    def create(self, valided_data):
        return Tour.objects.create(**valided_data)

    def validate_max_number_of_participants(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make number of participants lower or equal to zero!", )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Don't make price lower or equal to zero!", )
        if value > 99999:
            raise serializers.ValidationError("Normal price can not be higher than 99 999!", )
        return value

    def validate_date(self, value):
        if self.date_start > self.date_end:
            raise serializers.ValidationError("Start date cannot be before end date!", )
        return value

    # def validate_date_start(self, value):
    #     if value > self.date_end:
    #         raise serializers.ValidationError("Start date cannot be in the past", )
    #     return value
    #
    # def validate_date_end(self, value):
    #     if value > self.date_start:
    #         raise serializers.ValidationError("End date cannot be before start date", )
    #     return value


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=45)
    last_name = serializers.CharField(max_length=45)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

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

    def validate_password(self, value): #FIXME 'aiAufhalksjda' Password need to have at least one big letter
        if len(value) > 8:
                if any(char.isupper() for char in value):
                    if any(char.isdigit() for char in value):
                        return value
                    else:
                        raise serializers.ValidationError("Password need to have at least one number", )
                else:
                    raise serializers.ValidationError("Password need to have at least one big letter", )
        else:
            raise serializers.ValidationError("Short have to contain at least 8 characters", )


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    user = UserSerializer(many=True, read_only=True)
    date = serializers.DateField
    amount_of_adults = serializers.IntegerField()
    amount_of_children = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    tour = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ['id','user', 'date', 'amount_of_adults', 'amount_of_children', 'total_price', 'tour']

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

from django.db import models


#TODO check if python uses camel case or something else

class TourCategory(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Price(models.Model):
    normal_price = models.DecimalField(max_digits=7, decimal_places=2)
    reduced_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('normal_price',)

    def __str__(self):
        return "Normal price: " + str(self.normal_price) + " , reduced price: " + str(self.reduced_price)


class Place(models.Model):
    country = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    accommodation = models.CharField(max_length=45)

    class Meta:
        ordering = ('destination',)

    def __str__(self):
        return self.country + ", " + self.destination + ", " + self.accommodation


class Tour(models.Model): #FIXME foreign keys are showed as id keys but one field from this class would be more clear i.e.: type_of_tour: all-inclusive
    max_number_of_participants = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type_of_tour = models.ForeignKey(TourCategory, related_name='tour_category', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, related_name='place', on_delete=models.CASCADE)
    unit_price = models.ForeignKey(Price, related_name='price', on_delete=models.CASCADE)

    class Meta:
        ordering = ('type_of_tour',)

    def __str__(self):
        return self.place.__str__()


class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return self.email


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    dateOfReservation = models.DateTimeField(null=True, auto_created=True) #TODO check if date creates itself while POST method
    amount_of_adults = models.IntegerField()
    amount_of_children = models.IntegerField()
    total_price = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    tour = models.ForeignKey(Tour, related_name='tour', on_delete=models.CASCADE)

    class Meta:
        ordering = ('tour',)

    def __str__(self):
        return str(self.dateOfReservation) + " , amounts of adults: " + str(
            self.amount_of_adults) + " , amounts of children: " + str(
            self.amount_of_children) + " , total price: " + str(self.total_price) + " , tour: " + self.tour.__str__()

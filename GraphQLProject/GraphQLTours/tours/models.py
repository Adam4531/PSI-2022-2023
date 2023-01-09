from django.db import models


class Price(models.Model):
    normal_price = models.DecimalField(max_digits=7, decimal_places=2)
    reduced_price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('normal_price',)

    def __str__(self):
        return "Normal price: " + str(self.normal_price) + " , reduced price: " + str(self.reduced_price)


class Tour(models.Model):
    max_number_of_participants = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    place = models.CharField(max_length=45)
    unit_price = models.ForeignKey(Price, related_name='tours', on_delete=models.CASCADE)

    class Meta:
        ordering = ('max_number_of_participants',)

    def __str__(self):
        return "max number of participants: " + str(self.max_number_of_participants) + ", period from " + \
               self.date_start.__str__() + " to " + self.date_end.__str__() + ", price: " + str(self.price) + \
               ", destination: " + self.place.__str__() + \
               ", price per 1 person: " + str(self.unit_price)


class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return self.email


class Reservation(models.Model):  # TODO change field arguments 'null=True' to 'allow_null=True'
    user = models.ForeignKey('auth.User', related_name='reservations', on_delete=models.CASCADE)
    dateOfReservation = models.DateTimeField(null=True,
                                             auto_created=True)  # TODO check if date creates itself while POST method
    amount_of_adults = models.IntegerField()
    amount_of_children = models.IntegerField()
    total_price = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    tour = models.ForeignKey(Tour, related_name='reservations', on_delete=models.CASCADE)

    class Meta:
        ordering = ('tour',)

    def __str__(self):
        return str(self.dateOfReservation) + " , amounts of adults: " + str(
            self.amount_of_adults) + " , amounts of children: " + str(
            self.amount_of_children) + " , total price: " + str(self.total_price) + " , tour: " + self.tour.__str__()


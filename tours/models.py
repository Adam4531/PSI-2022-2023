from django.db import models


class TypeOfTour(models.Model):
    name = models.CharField(max_length=45, unique=True)

    # class Meta:
    #     ordering = ('name_of_type',)

    def __str__(self):
        return self.name


class Price(models.Model):
    normal_price = models.DecimalField(max_digits=7, decimal_places=2)
    reduced_price = models.DecimalField(max_digits=7, decimal_places=2)


class Places(models.Model):
    country = models.CharField(max_length=45)
    place = models.CharField(max_length=45)
    accommodation = models.CharField(max_length=45)

    def __str__(self):
        return self.country + ", " + self.place + ", " + self.accommodation


class Tour(models.Model):
    max_number_of_participants = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    type_of_tour = models.ForeignKey(TypeOfTour, related_name='type_of_tour', on_delete=models.CASCADE)
    place = models.ForeignKey(Places, related_name='places', on_delete=models.CASCADE)
    unit_price = models.ForeignKey(Price, related_name='price', on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ('place',)

    def __str__(self):
        return self.place


class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    # class Meta:
    #     ordering = ('email',)

    def __str__(self):
        return self.email


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    date = models.DateField
    amount_of_adults = models.IntegerField()
    amount_of_children = models.IntegerField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    tour = models.ForeignKey(Tour, related_name='tour', on_delete=models.CASCADE)

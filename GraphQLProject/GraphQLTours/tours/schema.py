import datetime

import graphene
from graphene_django import DjangoObjectType
from .models import Price, Tour, User, Reservation
from graphene import ObjectType, Field, String



class PriceType(DjangoObjectType):
    class Meta:
        model = Price
        fields = ('id', 'normal_price', 'reduced_price')


class TourType(DjangoObjectType):
    class Meta:
        model = Tour
        fields = ('id', 'max_number_of_participants', 'date_start', 'date_end', 'price', 'place', 'unit_price')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


class ReservationType(DjangoObjectType):
    class Meta:
        model = Reservation
        fields = ('id', 'user', 'dateOfReservation', 'amount_of_adults', 'amount_of_children', 'total_price', 'tour')


class Query(graphene.ObjectType):
    prices = graphene.List(PriceType)
    tours = graphene.List(TourType)
    users = graphene.List(UserType)
    reservations = graphene.List(ReservationType)
    reservations_by_place = graphene.List(ReservationType, place=graphene.String())


    def resolve_prices(root, info, **kwargs):
        return Price.objects.all()

    def resolve_tours(root, info, **kwargs):
        return Tour.objects.all()

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_reservations(root, info, **kwargs):
        return Reservation.objects.all()

    async def resolve_reservations_by_place(root, info, place: String):
        return Reservation.objects.all(place=place)



class InputPrice(graphene.InputObjectType):
       normal_price = graphene.Decimal(required=True)
       reduced_price = graphene.Decimal(required=True)

class CreatePrice(graphene.Mutation):
   class Arguments:
       input = InputPrice(required=True)
   price = graphene.Field(PriceType)

   @classmethod
   def mutate(cls, root, info, input):
       price = Price()
       price.normal_price = input.normal_price
       price.reduced_price = input.reduced_price
       price.save()
       return CreatePrice(price=price)

class UpdatePrice(graphene.Mutation):
   class Arguments:
       input = InputPrice(required=True)
       id = graphene.ID()
   price = graphene.Field(PriceType)

   @classmethod
   def mutate(cls, root, info, input , id):
       price = Price.objects.get(pk=id)
       price.normal_price = input.normal_price
       price.reduced_price = input.reduced_price
       price.save()
       return UpdatePrice(price=price)


class InputTour(graphene.InputObjectType):
    max_number_of_participants = graphene.Int()
    date_start = graphene.Date()
    date_end = graphene.Date()
    price = graphene.Decimal()
    place = graphene.String()
    unit_price = graphene.Field(InputPrice)


class CreateTour(graphene.Mutation):
    class Arguments:
        input = InputTour(required=True)

    tour = graphene.Field(TourType)

    @classmethod
    def mutate(cls, root, info, input_t):
        tour = Tour()
        tour.max_number_of_participants = input_t.max_number_of_participants
        tour.date_start = input_t.date_start
        tour.date_end = input_t.date_end
        tour.price = input_t.price
        tour.place = input_t.place
        tour.unit_price = input_t.unit_price
        tour.save()
        return CreatePrice(tour=tour)


class UpdateTour(graphene.Mutation):
    class Arguments:
        input = InputTour(required=True)
        id = graphene.ID()

    tour = graphene.Field(TourType)

    @classmethod
    def mutate(cls, root, info, input, id):
        tour = Tour.objects.get(pk=id)
        tour.max_number_of_participants = input.max_number_of_participants
        tour.date_start = input.date_start
        tour.date_end = input.date_end
        tour.price = input.price
        tour.place = input.place
        tour.unit_price = input.unit_price
        tour.save()
        return UpdateTour(tour=tour)

class DeleteTour(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Tour.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)



class InputUser(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = InputUser(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input):
        user = User()
        user.email = input.email
        user.password = input.password
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        input = InputUser(required=True)
        id = graphene.ID()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, input, id):
        user = User.objects.get(pk=id)
        user.email = input.email
        user.password = input.password
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.save()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = User.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)

class InputReservation(graphene.InputObjectType):
    user = graphene.Field(InputUser)
    dateOfReservation = graphene.DateTime()
    amount_of_adults = graphene.Int()
    amount_of_children = graphene.Int()
    total_price = graphene.Decimal()
    tour = graphene.Field(InputTour)

class CreateReservation(graphene.Mutation):
    class Arguments:
        input = InputReservation(required=True)

    reservation = graphene.Field(ReservationType)

    @classmethod
    def mutate(cls, root, info, input):
        reservation = Reservation()
        reservation.user = input.user
        # reservation.dateOfReservation = datetime.datetime.date()
        reservation.dateOfReservation = input.dateOfReservation
        reservation.amount_of_adults = input.amount_of_adults
        reservation.amount_of_children = input.amount_of_children
        reservation.total_price = input.total_price
        reservation.tour = input.tour
        reservation.save()
        return CreateReservation(reservation=reservation)

class UpdateReservation(graphene.Mutation):
    class Arguments:
        input = InputReservation(required=True)
        id = graphene.ID()

    reservation = graphene.Field(ReservationType)

    @classmethod
    def mutate(cls, root, info, input, id):
        reservation = Reservation.objects.get(pk=id)
        reservation.user = input.user
        # reservation.dateOfReservation = datetime.datetime.date()
        reservation.dateOfReservation = input.dateOfReservation
        reservation.amount_of_adults = input.amount_of_adults
        reservation.amount_of_children = input.amount_of_children
        reservation.total_price = input.total_price
        reservation.tour = input.tour
        reservation.save()
        return UpdateReservation(reservation=reservation)


class DeleteReservation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Reservation.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)


class Mutation(graphene.ObjectType):
   update_price = UpdatePrice.Field()
   create_price = CreatePrice.Field()
   update_tour = UpdateTour.Field()
   create_tour = CreateTour.Field()
   delete_tour = DeleteTour.Field()
   create_user = CreateUser.Field()
   update_user = UpdateUser.Field()
   delete_user = DeleteUser.Field()
   create_reservation = CreateReservation.Field()
   update_reservation = UpdateReservation.Field()
   delete_reservation = DeleteReservation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

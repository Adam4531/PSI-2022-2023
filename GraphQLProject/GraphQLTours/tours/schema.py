import graphene
from graphene_django import DjangoObjectType
from .models import Price, Tour, User, Reservation


class PriceType(DjangoObjectType):
    class Meta:
        model = Price
        fields = ('id', 'normal_price', 'reduced_price')


class TourType(DjangoObjectType):
    class Meta:
        model = Tour
        fields = ('id', 'max_number_of_participants', 'date_start' ,'date_end', 'price', 'place', 'unit_price')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')


class ReservationType(DjangoObjectType):
    class Meta:
        model = Reservation
        fields = ('id', 'user', 'dateOfReservation', 'amount_of_adults', 'amount_of_children', 'total_price', 'tour')


class Query(graphene.ObjectType):
    price = graphene.List(PriceType)
    tour = graphene.List(TourType)
    user = graphene.List(UserType)
    reservation = graphene.List(ReservationType)

    def resolve_prices(root, info, **kwargs):
        return Price.objects.all()

    def resolve_tours(root, info, **kwargs):
        return Tour.objects.all()

    def resolve_users(root, info, **kwargs):
        return User.objects.all()

    def resolve_reservations(root, info, **kwargs):
        return Reservation.objects.all()


class UpdatePrice(graphene.Mutation):
   class Arguments:
       normal_price = graphene.Decimal(required=True)
       reduced_price = graphene.Decimal(required=True)
       id = graphene.ID()
   price = graphene.Field(PriceType)

   @classmethod
   def mutate(cls, root, info, normal_price, reduced_price, id):
       price = Price.objects.get(pk=id)
       price.normal_price = normal_price
       price.reduced_price = reduced_price
       price.save()
       return UpdatePrice(price=price)


class CreatePrice(graphene.Mutation):
   class Arguments:
       normal_price = graphene.Decimal(required=True)
       reduced_price = graphene.Decimal(required=True)
   price = graphene.Field(PriceType)

   @classmethod
   def mutate(cls, root, info, normal_price, reduced_price):
       price = Price()
       price.normal_price = normal_price
       price.reduced_price = reduced_price
       price.save()
       return CreatePrice(price=price)







class Mutation(graphene.ObjectType):
   update_price = UpdatePrice.Field()
   create_price = CreatePrice.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

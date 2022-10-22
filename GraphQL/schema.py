import graphene
from graphene_django import DjangoObjectType

from cars.models import Car


class CarType(DjangoObjectType):
    class Meta:
        model = Car
        fields = '__all__'


class Query(graphene.ObjectType):
    all_cars = graphene.List(CarType)
    cars_by_brand = graphene.List(CarType, brand=graphene.String(required=True))

    @staticmethod
    def resolve_all_cars(root, info):
        return Car.objects.all()

    @staticmethod
    def resolve_cars_by_brand(root, info, brand):
        return Car.objects.filter(brand=brand)


class CarInput(graphene.InputObjectType):
    id = graphene.ID()
    vin = graphene.String()
    title = graphene.String()
    brand = graphene.String()
    price = graphene.Int()
    model_year = graphene.Int()


class CreateCar(graphene.Mutation):
    class Arguments:
        data = CarInput(required=True)

    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, data):
        car_instance = Car(
            vin=data.vin,
            title=data.title,
            brand=data.brand,
            price=data.price,
            model_year=data.model_year
        )
        car_instance.save()
        return CreateCar(car=car_instance)


class UpdateCar(graphene.Mutation):
    class Arguments:
        data = CarInput(required=True)

    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, data):
        car_instance = Car.objects.get(pk=data.id)

        if car_instance:
            car_instance.vin = data.vin
            car_instance.title = data.title
            car_instance.brand = data.brand
            car_instance.price = data.price
            car_instance.model_year = data.model_year
            car_instance.save()

            return UpdateCar(car=car_instance)

        return UpdateCar(car=None)


class DeleteCar(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    car = graphene.Field(CarType)

    @staticmethod
    def mutate(root, info, id):
        car_instance = Car.objects.get(pk=id)
        car_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_car = CreateCar.Field()
    update_car = UpdateCar.Field()
    delete_car = DeleteCar.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

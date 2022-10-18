import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Car(models.Model):

    class Meta:
        db_table = 'car'

    vin = models.CharField(max_length=100, verbose_name='VIN', null=False, blank=False, unique=True)
    title = models.CharField(max_length=100, verbose_name='Название', null=False, blank=False)
    brand = models.CharField(max_length=100, verbose_name='Бренд', null=False, blank=False)
    price = models.IntegerField(verbose_name='Цена (руб)')
    model_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1899), MaxValueValidator(datetime.date.today().year)]
    )


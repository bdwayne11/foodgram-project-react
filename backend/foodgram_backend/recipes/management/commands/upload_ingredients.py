import pandas
from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    help = 'Loads data from csv'

    def handle(self, *args, **options):
        users_data = pandas.read_csv('data/ingredients.csv', sep=',')

        ingredients = [
            Ingredients(
                name=row[0],
                measurement_unit=row[1]
            ) for _, row in users_data.iterrows()
        ]

        Ingredients.objects.bulk_create(ingredients)
        print('Успешная загрузка в БД!')

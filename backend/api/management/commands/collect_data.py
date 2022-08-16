import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from api.models import Ingredient, Tag
from users.models import User


DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                data = csv.reader(csv_file)
                for row in data:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
        except FileNotFoundError:
            raise CommandError('Добавьте файл ingredients в директорию data')
        self.stdout.write('Записи добавленны в базу данных')
        try:
            Tag.objects.get_or_create(name='Мясо',
                                      color='#FF0000',
                                      slug='meat')
            Tag.objects.get_or_create(name='Веган',
                                      color='#00FF00',
                                      slug='vegan')
            Tag.objects.get_or_create(name='Прочее',
                                      color='#EEE8AA',
                                      slug='pr')
            Tag.objects.get_or_create(name='Звезда мишлен',
                                      color='#4682B4',
                                      slug='mishk')
        except FileNotFoundError:
            raise CommandError('Ошибка в добавлении тегов')
        self.stdout.write('Теги добавленны в базу данных')
        # try:
        #     User.objects.get_or_create(
        #         username='test',
        #         email='test@mail.com',
        #         password='pbkdf2_sha256$150000$04dIcOWi9tFx$RIuSYggPvu/sxyGR2yBTpxj5FkNhuj7upAlMY/UTiPM=',
        #         #Qwerty12345678!
        #         first_name='test_name',
        #         last_name='test_lastname',
        #         )
        # except FileNotFoundError:
        #     raise CommandError('Ошибка в добавлении пользователя')
        # self.stdout.write('Тестовый пользователь добавлен в базу данных')

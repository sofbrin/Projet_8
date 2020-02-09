from abc import ABC

from django.core.management.base import BaseCommand
from products.dbBuilder import *


class Command(BaseCommand, ABC):
    help = "create the database with categories and products by entering a number between 5 & 20"

    def add_arguments(self, parser):

        parser.add_argument('nb_categories',  type=int, default=15, nargs='?', help='choisir le nb de catégories')

    def handle(self, *args, **options):
        print(options['nb_categories'])
        select_categories(options['nb_categories'])


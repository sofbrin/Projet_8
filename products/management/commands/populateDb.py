from abc import ABC

from django.core.management.base import BaseCommand, CommandError
from products.dbBuilder import *


class Command(BaseCommand, ABC):
    help = "Populate the database with OpenFoodFacts' data"

    def handle(self, *args, **options):
        select_categories()


from django.core.management.base import BaseCommand
from main.data_storage.models import StockSector, Company

MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "Seed database."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('Done seeding.')

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode.lower() == MODE_CLEAR:
        return

    # Seed data
    create_stock_sectors()

def clear_data():
    """Deletes all the table data"""
    StockSector.objects.all().delete()

def create_stock_sectors():
    """Creates stock sectors"""
    names = ['Communication Services', 'Consumer Discretionary', 'Consumer Staples', 'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology', 'Materials', 'Real Estate', 'Utilities']
    for index, name in enumerate(names, start=1):
        sector = StockSector(id=index, name=name)
        sector.save()
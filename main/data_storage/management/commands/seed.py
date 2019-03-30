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
    create_top_companies()

def clear_data():
    """Deletes all the table data"""
    StockSector.objects.all().delete()

def create_stock_sectors():
    """Creates stock sectors"""
    names = ["Energy", "Materials", "Industrials", "Consumer Discretionary", "Consumer Staples", "Health Care", "Financials", "Information Technology", "Telecommunication Services", "Utilities", "Real Estate"]
    for index, name in enumerate(names, start=1):
        sector = StockSector(id=index, name=name)
        sector.save()

def create_top_companies():
    sector_healthcare = StockSector.objects.get(name="Health Care")
    sector_tech = StockSector.objects.get(name="Information Technology")
    sector_fin = StockSector.objects.get(name="Financials")

    tndm = Company(id=1, name="Tandem Diabetes Care, Inc.", symbol="TNDM", sector=sector_healthcare)
    tndm.save()

    nvta = Company(id=2, name="Invitae Corporation", symbol="NVTA", sector=sector_healthcare)
    nvta.save()

    ins = Company(id=3, name="Intelligent Systems Corporation", symbol="INS", sector=sector_tech)
    ins.save()

    tpnl = Company(id=4, name="3Pea Intl Inc", symbol="TPNL", sector=sector_tech)
    tpnl.save()

    cme = Company(id=5, name="CME Group Inc.", symbol="CME", sector=sector_fin)
    cme.save()
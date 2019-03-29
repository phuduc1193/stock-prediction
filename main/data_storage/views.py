from rest_framework import viewsets, generics
from main.data_storage.models import Company, StockPrice, StockSector
from main.data_storage.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer

# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StockSectorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stock sectors to be viewed or edited.
    """
    queryset = StockSector.objects.all()
    serializer_class = StockSectorSerializer

class StockPriceList(generics.ListAPIView):
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the stock prices
        for the stock symbol.
        """
        symbol = self.kwargs['symbol']
        company = Company.objects.get(stock_symbol=symbol)
        return StockPrice.objects.filter(company=company)
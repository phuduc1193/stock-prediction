from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from main.data_storage.models import Company, StockPrice, StockSector
from main.data_storage.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer
from django.shortcuts import get_object_or_404

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

class StockPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stock prices to be viewed or edited.
    """
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        """
        """
        symbol = self.request.query_params.get('symbol', None)
        if symbol is not None:
            company = get_object_or_404(Company, symbol=symbol)
            self.queryset = self.queryset.filter(company=company)
        return self.queryset
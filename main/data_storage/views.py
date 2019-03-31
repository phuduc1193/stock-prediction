from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from main.data_storage.models import Company, StockPrice, StockSector
from main.data_storage.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer
from main.data_storage.data_center import DataCenter

# Create your views here.
class CompanyViewSet(ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StockSectorViewSet(ModelViewSet):
    """
    API endpoint that allows stock sectors to be viewed or edited.
    """
    queryset = StockSector.objects.all()
    serializer_class = StockSectorSerializer

class StockPriceViewSet(ModelViewSet):
    """
    API endpoint that allows stock prices to be viewed or edited.
    """
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol', None)
        if symbol is not None:
            try:
                company = Company.objects.get(symbol=symbol)
            except Exception as err:
                dc = DataCenter(symbol=symbol)
                company = dc.get_company()
                if company is None:
                    from django.http import Http404
                    raise Http404()
                company.save()

            self.queryset = self.queryset.filter(company=company)
        return self.queryset
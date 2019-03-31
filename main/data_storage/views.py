from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from main.data_storage.models import Company, StockPrice, StockSector
from main.data_storage.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer
from main.data_storage.data_center import DataCenter

# Create your views here.
class CompanyViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'symbol'

    def retrieve(self, request, *args, **kwargs):
        symbol = kwargs.get('symbol', None)
        if symbol is None:
            raise Http404()
        symbol = symbol.upper()
        try:
            instance = Company.objects.get(symbol=symbol)
        except Exception:
            instance = load_company(symbol)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class StockSectorViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows stock sectors to be viewed or edited.
    """
    queryset = StockSector.objects.all()
    serializer_class = StockSectorSerializer
    lookup_field = 'slug'

class StockPriceViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows stock prices to be viewed or edited.
    """
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol', None)
        if symbol is not None:
            symbol = symbol.upper()
            try:
                company = Company.objects.get(symbol=symbol)
            except Exception:
                load_company(symbol)

            self.queryset = self.queryset.filter(company=company)
        return self.queryset

def load_company(symbol):
    dc = DataCenter(symbol=symbol)
    company = dc.get_company()
    if company is None:
        raise Http404()
    company.save()
    return company
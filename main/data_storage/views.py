from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from main.data_storage.models import Company, StockPrice, StockSector
from main.data_storage.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer
from main.data_storage.data_center import DataCenter

import pandas as pd

# Create your views here.
class CompanyViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows companies to be viewed.
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
    API endpoint that allows stock sectors to be viewed.
    """
    queryset = StockSector.objects.all()
    serializer_class = StockSectorSerializer
    lookup_field = 'slug'

class StockPriceViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows stock prices to be viewed.
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
                company = load_company(symbol)

            load_stock_prices(company)
            self.queryset = self.queryset.filter(company=company)
        return self.queryset

def load_company(symbol):
    df = DataCenter(symbol=symbol).get_company()
    if df is None:
        raise Http404()
        
    sector = StockSector.objects.get(name__icontains=str(df['sector'].values[0]))
    company = Company(name=df['companyName'].values[0], symbol=df['symbol'].values[0], description=df['description'].values[0], website=df['website'].values[0], ceo=df['CEO'].values[0], sector=sector)
    if company is None:
        raise Http404()
    company.save()
    return company

def load_stock_prices(company):
    symbol = company.symbol
    dc = DataCenter(symbol=symbol)
    df = dc.get_intraday(outputsize='full')
    stored_data = StockPrice.objects.all().filter(company=company)
    list_existed_timestamp = [pd.Timestamp(o.timestamp) for o in stored_data]
    df = df[~df.timestamp.isin(list_existed_timestamp)]
    stock_prices = [StockPrice(**kwargs) for kwargs in df.to_dict(orient='records')]
    for stock_price in stock_prices:
        stock_price.company = company
    return StockPrice.objects.bulk_create(stock_prices)
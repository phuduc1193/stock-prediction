from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from main.app.models import Company, StockPrice, StockSector, StockPrediction
from main.app.serializers import CompanySerializer, StockPriceSerializer, StockSectorSerializer, StockPredictionSerializer
from main.app.datacenter import DataCenter
from main.app.paginations import LargeResultsSetPagination
from main.app.stocker import Stocker

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

        instance = load_company(symbol)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='stock-prices')
    def stock_prices(self, request, symbol=None, *args, **kwargs):
        if symbol is None:
            raise Http404()
        symbol = symbol.upper()
        
        company = load_company(symbol)

        instances = StockPrice.objects.all().filter(company=company)
        if not instances:
            instances = load_stock_prices(company)

        self.pagination_class = LargeResultsSetPagination
        self.ordering_fields = ('-date')
        page = self.paginate_queryset(instances)
        if page is not None:
            serializer = StockPriceSerializer(page, many=True, *args, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = StockPriceSerializer(instances, many=True, *args, **kwargs)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def predict(self, request, symbol=None, *args, **kwargs):
        if symbol is None:
            raise Http404()
        symbol = symbol.upper()

        stocker = Stocker(symbol)
        df = stocker.predict_future()
        df = df.rename(columns={'Date': 'date'})
        df['symbol'] = symbol
        df = df[['symbol', 'estimate', 'upper', 'lower']]
        instances = [StockPrediction(**kwargs) for kwargs in df.to_dict(orient='records')]

        self.pagination_class = LargeResultsSetPagination
        self.ordering_fields = ('-date')
        page = self.paginate_queryset(instances)
        if page is not None:
            serializer = StockPredictionSerializer(page, many=True, *args, **kwargs)
            return self.get_paginated_response(serializer.data)

        serializer = StockPredictionSerializer(instances, many=True, *args, **kwargs)
        print(serializer)
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
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        symbol = self.request.query_params.get('symbol', None)
        if symbol is None:
            return self.queryset

        company = load_company(symbol)
        load_stock_prices(company)
        self.queryset = self.queryset.filter(company=company)
        return self.queryset

def load_company(symbol):
    try:
        return Company.objects.get(symbol=symbol)
    except Exception:
        pass

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
    df = dc.get_daily(outputsize='full')
    df = df.drop(columns=['Adj. Open', 'Adj. Close', 'Dividend', 'Split Coefficient'])
    df.columns = ['open', 'close', 'high', 'low', 'volume', 'date']
    stored_data = StockPrice.objects.all().filter(company=company)
    list_existed_date = [pd.Timestamp(o.date) for o in stored_data]
    df = df[~df.date.isin(list_existed_date)]
    stock_prices = [StockPrice(**kwargs) for kwargs in df.to_dict(orient='records')]
    for stock_price in stock_prices:
        stock_price.company = company
    return StockPrice.objects.bulk_create(stock_prices)
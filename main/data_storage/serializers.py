from rest_framework import serializers
from main.data_storage.models import Company, StockPrice, StockSector

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    sector = serializers.ReadOnlyField(source='sector.name')
    CEO = serializers.ReadOnlyField(source='ceo')
    stock_price_url =  serializers.HyperlinkedIdentityField(view_name='company-stock-prices', lookup_field='symbol')

    class Meta:
        model = Company
        fields = ('url', 'name', 'symbol', 'sector', 'website', 'CEO', 'description', 'stock_price_url')
        extra_kwargs = {
            'url': {'lookup_field': 'symbol'},
        }
        read_only_fields = ('id', 'sector')

class StockPriceSerializer(serializers.HyperlinkedModelSerializer):
    symbol = serializers.ReadOnlyField(source='company.symbol')
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = StockPrice
        fields = ('company', 'symbol', 'open', 'close', 'high', 'low', 'volume', 'timestamp')
        read_only_fields = ('id', 'company','symbol', 'timestamp')

class StockSectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockSector
        fields = ('url', 'name')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
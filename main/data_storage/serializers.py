from rest_framework import serializers
from main.data_storage.models import Company, StockPrice, StockSector

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    sector = serializers.ReadOnlyField(source='sector.name')
    symbol = serializers.ReadOnlyField(source='stock_symbol')
    class Meta:
        model = Company
        fields = ('url', 'name', 'symbol', 'sector')

class StockPriceSerializer(serializers.HyperlinkedModelSerializer):
    symbol = serializers.ReadOnlyField(source='company.stock_symbol')
    class Meta:
        model = StockPrice
        fields = ('url', 'symbol', 'open', 'close', 'high', 'low', 'timestamp')

class StockSectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockSector
        fields = ('url', 'name')
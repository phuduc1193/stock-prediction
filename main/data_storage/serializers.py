from rest_framework import serializers
from main.data_storage.models import Company, StockPrice, StockSector

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    sector = serializers.ReadOnlyField(source='sector.name')
    class Meta:
        model = Company
        fields = ('url', 'name', 'symbol', 'sector')
        read_only_fields = ('id',)

class StockPriceSerializer(serializers.HyperlinkedModelSerializer):
    symbol = serializers.ReadOnlyField(source='company.symbol')
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = StockPrice
        fields = ('url', 'company', 'symbol', 'open', 'close', 'high', 'low', 'timestamp')
        read_only_fields = ('id', 'company','symbol', 'timestamp')

class StockSectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StockSector
        fields = ('url', 'name')
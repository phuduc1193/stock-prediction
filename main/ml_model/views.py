from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from main.ml_model.models import StockModel
from main.ml_model.stocker import Stocker

class Predict(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()
        stock = Stocker(symbol)
        model, future = stock.create_prophet_model(days=7)
        return Response(future, status=status.HTTP_200_OK)
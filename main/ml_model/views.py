from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from main.ml_model.models import StockModel
from main.ml_model.ml import train, predict

class Train(APIView):
    def post(self, request):
        symbol = request.data.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()

        try:
            stock_model = get_object_or_404(StockModel, symbol=symbol)
            return Response(status=status.HTTP_200_OK)
        except Exception:
            pass

        try:
            model_name, scaler_name = train(symbol)
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        stock_model = StockModel(symbol=symbol, model_name=model_name, scaler_name=scaler_name)
        stock_model.save()

        return Response({'code': '201', 'message': 'Created'}, status=status.HTTP_201_CREATED)

    def put(self, request):
        symbol = request.data.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()

        stock_model = get_object_or_404(StockModel, symbol=symbol)

        stock_model.model_name, stock_model.scaler_name = train(symbol)
        stock_model.save()

        return Response({'code': '200', 'message': 'Updated'}, status=status.HTTP_200_OK)

class Predict(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()
        
        stock_model = get_object_or_404(StockModel, symbol=symbol)
        prediction = predict(symbol, stock_model.scaler_name, stock_model.model_name)
        return Response(prediction.item(0), status=status.HTTP_200_OK)
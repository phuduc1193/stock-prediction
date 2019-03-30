import os
import pandas as pd
import pickle
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from main.data_storage.models import Company, StockPrice

class StockPredictionViewSet(ViewSet):
    '''
    Train and predic stock price for a stock `symbol`
    '''
    def create(self, request, format=None):
        symbol = request.data.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        
        symbol = symbol.upper()
        model_name = 'model.{}.sav'.format(symbol)
        scaler_name = 'scaler.{}.sav'.format(symbol)

        company = get_object_or_404(Company, symbol=symbol)
        stock_prices = StockPrice.objects.filter(company=company)
        try:
            #train data
            clf = {'string': 'string'}
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.MODEL_ROOT, model_name)
        with open(path, 'wb') as file:
            pickle.dump(clf, file)
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        predictions = []
        for entry in request.data:
            model_name = entry.pop('model_name')
            path = os.path.join(settings.MODEL_ROOT, model_name)
            with open(path, 'rb') as file:
                model = pickle.load(file)
            try:
                result = model.predict(pd.DataFrame([entry]))
                predictions.append(result[0])

            except Exception as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        return Response(predictions, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = StockPrice.objects.all()
        symbol = self.request.query_params.get('symbol', None)
        if symbol is not None:
            company = get_object_or_404(Company, symbol=symbol)
            queryset = queryset.filter(company=company)
        return queryset
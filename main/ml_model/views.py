import os
import pandas as pd
import pickle
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from main.data_storage.models import Company, StockPrice
from main.ml_model.models import StockModel

class Train(APIView):
    def post(self, request):
        symbol = request.data.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()

        try:
            stock_model = StockModel.objects.get(symbol=symbol)
            return Response(status=status.HTTP_200_OK)
        except StockModel.DoesNotExist:
            stock_model = None

        model_name = 'model.{}.sav'.format(symbol)
        scaler_name = 'scaler.{}.sav'.format(symbol)

        try:
            company = Company.objects.get(symbol=symbol)
        except Exception as err:
            return Response(str(err), status=status.HTTP_404_NOT_FOUND)

        try:
            stock_prices = StockPrice.objects.get(company=company)
        except Exception as err:
            return Response(str(err), status=status.HTTP_404_NOT_FOUND)

        try:
            #train data
            clf = {'string': 'string'}
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.MODEL_ROOT, model_name)
        with open(path, 'wb') as file:
            pickle.dump(clf, file)
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request):
        symbol = request.data.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)
        symbol = symbol.upper()

        try:
            stock_model = StockModel.objects.get(symbol=symbol)
            
            ## retrain data
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(str(err), status=status.HTTP_404_NOT_FOUND)

class Predict(APIView):
    def get(self, request):
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
        print(self.request)
        symbol = self.request.query_params.get('symbol', None)
        if symbol is None:
            return Response('Missing required key `symbol` in params', status=status.HTTP_400_BAD_REQUEST)

        company = get_object_or_404(Company, symbol=symbol)
        queryset = StockPrice.objects.filter(company=company)
        return queryset
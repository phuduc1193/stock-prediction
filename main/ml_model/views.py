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
from main.ml_model.stocker import Stocker

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
        symbol = symbol.upper()
        stock = Stocker(symbol)
        model, future = stock.create_prophet_model(days=7)
        return Response(future, status=status.HTTP_200_OK)

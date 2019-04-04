from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers

from main.data_storage.views import CompanyViewSet, StockSectorViewSet, StockPriceViewSet
from main.ml_model.views import Predict

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'stock-sectors', StockSectorViewSet)
router.register(r'stock-prices', StockPriceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    url('api/model/predict', Predict.as_view(), name="predict"),
    url('api/model/predict/', Predict.as_view(), name="predict"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
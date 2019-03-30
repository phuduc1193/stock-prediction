from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from main.data_storage import views
from main.ml_model.views import StockPredictionViewSet

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'stock-sectors', views.StockSectorViewSet)
router.register(r'stock-prices', views.StockPriceViewSet)
router.register(r'ml', StockPredictionViewSet, basename='ml')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
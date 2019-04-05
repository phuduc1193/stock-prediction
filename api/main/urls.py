from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers

from main.app.views import CompanyViewSet, StockSectorViewSet, StockPriceViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'stock-sectors', StockSectorViewSet)
router.register(r'stock-prices', StockPriceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
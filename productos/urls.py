from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet

router = DefaultRouter()
router.register('products', ProductoViewSet, basename='producto')

urlpatterns = router.urls
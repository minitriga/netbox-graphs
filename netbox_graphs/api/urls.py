from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import GraphViewSet

router = routers.DefaultRouter()
router.register(r"(?P<model>.+)", GraphViewSet, basename="return-graphs")

urlpatterns = router.urls

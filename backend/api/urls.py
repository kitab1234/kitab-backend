from rest_framework.routers import DefaultRouter
from alkitaab.api.urls import user_router, custom_user_router, ibadat_router, scale_router, ibadat_item_router
from django.urls import path, include
router = DefaultRouter()
router.registry.extend(user_router.registry)
router.registry.extend(custom_user_router.registry)
router.registry.extend(ibadat_router.registry)
router.registry.extend(scale_router.registry)
router.registry.extend(ibadat_item_router.registry)
urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path
from .views import (
    ProductListAPIView,
    DesignRequestCreateAPIView,
    DesignRequestDetailAPIView
)

app_name = 'core'

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('design-requests/', DesignRequestCreateAPIView.as_view(),
         name='design-request-create'),
    path('design-requests/<slug:slug>/',
         DesignRequestDetailAPIView.as_view(), name='design-request-detail'),
]

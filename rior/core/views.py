from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db import transaction

from .models import Product, DesignRequest
from .serializers import (
    ProductSerializer,
    DesignRequestCreateSerializer,
    DesignRequestResultSerializer
)
from .utils import mock_ai_process


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DesignRequestCreateAPIView(generics.GenericAPIView):
    parser_classes   = (MultiPartParser, FormParser)
    serializer_class = DesignRequestCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dr = serializer.save()

        # Call our mock AI
        ai_out = mock_ai_process(
            dr.floor_plan.path,
            dr.door_height,
            dr.ceiling_height,
            dr.interior_photo.path
        )

        dr.ai_response = ai_out
        # Use floor_plan as placeholder for design image
        dr.design_image = dr.floor_plan
        dr.save()

        # Attach only existing products to avoid FK errors
        product_ids = [p.get('id') for p in ai_out.get('products', [])]
        existing_products = Product.objects.filter(id__in=product_ids)
        dr.products.set(existing_products)

        result_serializer = DesignRequestResultSerializer(dr, context={'request': request})
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)


class DesignRequestDetailAPIView(generics.RetrieveAPIView):
    lookup_field     = 'slug'
    queryset         = DesignRequest.objects.all()
    serializer_class = DesignRequestResultSerializer

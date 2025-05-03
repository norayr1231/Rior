from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.db import transaction

from .models import Product, DesignRequest
from .serializers import (
    ProductSerializer,
    DesignRequestCreateSerializer,
    DesignRequestResultSerializer,
    DesignRequestListSerializer
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
        data = serializer.validated_data

        ai_out = mock_ai_process(
            data['floor_plan'],
            data['interior_photo'],
            data['door_height'],
            data['ceiling_height']
        )

        dr = DesignRequest.objects.create(
            name = data['name'],
            floor_plan=data['floor_plan'],
            design_image=data.get('interior_photo'),
            door_height=data['door_height'],
            ceiling_height=data['ceiling_height'],
            area=ai_out.get('area', 0),
            perimeter=ai_out.get('perimeter', 0),
            wall_area=ai_out.get('perimeter', 0) * data['ceiling_height'],
            ai_response=ai_out
        )

        product_ids = [p.get('id') for p in ai_out.get('products', [])]
        existing_products = Product.objects.filter(id__in=product_ids)
        dr.products.set(existing_products)

        result_serializer = DesignRequestResultSerializer(dr, context={'request': request})
        return Response({
            'status': 'success',
            'data': result_serializer.data['slug'],
            
        }, status=status.HTTP_201_CREATED)


class DesignRequestDetailAPIView(generics.RetrieveAPIView):
    lookup_field     = 'slug'
    queryset         = DesignRequest.objects.all()
    serializer_class = DesignRequestResultSerializer

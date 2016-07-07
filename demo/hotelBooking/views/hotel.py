from django.core.paginator import Paginator, EmptyPage
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from hotelBooking import Hotel
from hotelBooking.core.serializers.hotels import HouseSerializer, HotelSerializer
from hotelBooking.core.utils.serializer_helpers import wrapper_dict
from hotelBooking.core.viewsets import WithCustomJsonViewSetMixin

from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from hotelBooking.core.models.houses import House

class HotelViewSet(DynamicModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer.data)
            print(type(serializer.data))
            data = serializer.data
            meta = self.paginator.get_page_metadata()
            return Response(wrapper_dict(data,code=100,message='成功'))
        serializer = self.get_serializer(queryset, many=True)

        return Response(wrapper_dict(serializer.data))


class HouseViewSet(DynamicModelViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultJsonResponse(res_data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data =  self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(res_data=serializer.data)

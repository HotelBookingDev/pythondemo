from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from hotelBooking import Hotel
from hotelBooking.serializers import HotelSerializer, HouseSerializer

from . import DefaultJsonResponse,House

class HotelViewSet(RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(request.POST)
        print(request.GET)
        print(request.query_params)
        city_id = request.query_params.get('cityId')
        hotels = queryset.all()
        if city_id is not  None:
            hotels =hotels.filter(city_id=city_id).all()
        try:
            page = request.query_params.get('page',1)
            if int(page) < 1 :
                page =1
        except ValueError as e:
            print('catch error'+e.__str__())

        print(hotels)
        paginator = Paginator(hotels,1)
        try:
            backHotels = paginator.page(page)
            serializers = self.serializer_class(backHotels,many=True,excludes=('houses',))
        except EmptyPage as e:
            return DefaultJsonResponse(code=-100, message='没有更多数据')
        return DefaultJsonResponse(res_data={'hotels': serializers.data})



# class HotelListView(ListAPIView):
#     serializer_class = HotelSerializer
#     queryset = Hotel.objects.all()
#
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     print(request.POST)
    #     print(request.GET)
    #     print(request.query_params)
    #     city_id = request.query_params.get('cityId')
    #     hotels =queryset.filter(city_id=city_id)
    #     try:
    #         page = request.query_params.get('page',1)
    #         if int(page) < 1 :
    #             page =1
    #     except ValueError as e:
    #         print('catch error'+e.__str__())
    #
    #     print(hotels)
    #     paginator = Paginator(hotels,1)
    #     try:
    #         backHotels = paginator.page(page)
    #         serializers = self.serializer_class(backHotels,many=True,excludes=('houses',))
    #     except EmptyPage as e:
    #         return DefaultJsonResponse(code=-100, message='没有更多数据')
    #     return DefaultJsonResponse(res_data={'hotels': serializers.data})

class HouseViewSet(viewsets.GenericViewSet):

    serializer_class = HouseSerializer
    queryset = House.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return DefaultJsonResponse(res_data={'house':serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data =  self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(res_data=serializer.data)

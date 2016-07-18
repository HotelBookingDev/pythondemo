from dynamic_rest.viewsets import DynamicModelViewSet, WithDynamicViewSetMixin
from hotelBooking.core.utils import hotel_query_utils
from hotelBooking.core.utils.serializer_helpers import wrapper_response_dict
from hotelBooking.models.hotel import Hotel
from hotelBooking.models.hotel import Room
from hotelBooking.serializers import RoomSerializer, HotelSerializer
from hotelBooking.utils.AppJsonResponse import DefaultJsonResponse
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class HotelViewSet(WithDynamicViewSetMixin,ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(serializer.data))

    def list(self, request, *args, **kwargs):
        print(self.filter_backends)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            print(serializer.data)
            print(type(serializer.data))
            data = serializer.data
            meta = self.paginator.get_page_metadata()
            return Response(wrapper_response_dict(data, code=100, message='成功'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(wrapper_response_dict(serializer.data))

    @detail_route(methods=['GET',],url_path='types/')
    def query_room_types(self,request):
        # 目前使用在，商家端新建room的时候
        self.get_object()
        return Response('success')


    def get_queryset(self, queryset=None):
        if (queryset == None):
            queryset = self.queryset
        checkinTime = self.request.query_params.get('checkinTime',None)
        checkoutTime = self.request.query_params.get('checkoutTime',None)
        cityId = self.request.query_params.get('cityId',None)
        if (checkinTime and checkoutTime and cityId):
            return hotel_query_utils.query(queryset, cityId, checkinTime, checkoutTime)
        else:
            return queryset


# class RoomTypeViewSet(viewsets.ViewSet):
#     serializer_class = RoomTypeSerializer
#
#     def list(self,request,hotel_pk=None):
#
#         queryset = Room.objects.filter(hotel__id=hotel_pk)
#         serializer = self.serializer_class(queryset.all(),many=True)
#         return Response(wrapper_response_dict(data=serializer.data))

# class HotelDetialView()

class RoomViewSet(DynamicModelViewSet):

    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(wrapper_response_dict(serializer.data))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data =  self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return DefaultJsonResponse(res_data=serializer.data)


# todo 根据酒店id   返回 该酒店目前支持的房型
def query_hotel_room_type(request):
    pass
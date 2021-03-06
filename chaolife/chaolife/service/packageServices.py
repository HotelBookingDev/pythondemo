#-*- coding: utf-8 -*-
from chaolife.models import HotelPackageOrder
from chaolife.models.products import RoomPackage,RoomDayState
from datetime import datetime, timedelta


def createRoomDaysFormRoomPackage(roomPackage):
    """
    创建 对应roompackage 的 30天周期房态
    这个方法方法在celery中调用
    :param roomPackage:
    :return:
    """
    roomStates = []
    day = datetime.today().date()
    # assert day == roomPackage.created_on.date()
    for i in range(0, 30):
        print(day.strftime('%Y-%m-%d'))
        print(i)
        obj = RoomDayState(agent=roomPackage.owner,
                           roomPackage=roomPackage,
                           room=roomPackage.room,
                           hotel=roomPackage.hotel,
                           city=roomPackage.hotel.city,
                           d_point=roomPackage.default_d_point,
                           d_price=roomPackage.default_d_price,
                           s_point=roomPackage.default_s_point,
                           s_price=roomPackage.default_s_price,
                           state=RoomDayState.ROOM_STATE_EMPTY,
                           date=day.strftime('%Y-%m-%d')
                           )
        roomStates.append(obj)
        day += timedelta(days=1)
    print('执行完毕。创建了对象'.format(len(roomStates)))
    RoomDayState.objects.bulk_create(roomStates)


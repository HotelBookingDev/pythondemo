from django.utils import timezone

from django.db import models
from . import BaseModel
from ...utils.fiels import ListField
from hotelBooking.models import User
from django.utils.translation import ugettext_lazy as _
class Installation(BaseModel):
    valid = models.BooleanField(default=True)
    timeZone = models.CharField(max_length=200,default=timezone.now)
    channels = ListField(default=["public", "private"],verbose_name='订阅渠道',null=True)
    deviceToken = models.CharField(max_length=200,null=True)
    installationId = models.CharField(max_length=200,null=True,verbose_name='设备id')
    deviceType = models.CharField(max_length=200,default="android")
    badge = models.BigIntegerField(default=0,verbose_name='ios badge数')
    deviceProfile = models.CharField(max_length=200,default="")
    user = models.ForeignKey(User,null=True,verbose_name='绑定用户')
    active = models.BooleanField(_('active?'),default=True)

    class Meta:
        app_label = 'hotelBooking'
        verbose_name = "App已安装设备"
        verbose_name_plural = "设备"

    def __unicode__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)

    def __str__(self):
        return '%s-Token %s'%(self.deviceType,self.deviceToken)


def validate_unique_deviceToken_or_null(value):
    if value != None:
        Installation.objects.update_or_create()
        pass
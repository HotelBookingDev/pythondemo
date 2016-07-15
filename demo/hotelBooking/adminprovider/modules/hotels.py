from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .. import Hotel,HotelImg,House,HousePackage



class HotelLogoInline(admin.TabularInline):
    model = HotelImg

class HouseInline(admin.StackedInline):
    show_change_link = True
    model = House

class HousePackageInline(admin.StackedInline):
    show_change_link = True
    model = HousePackage
    verbose_name = '套餐'
    verbose_name_plural = '套餐'
    extra = 0
    fields = ('need_point','front_price','breakfast','owner','detail','checked','active','house')



class HotelAdmin(ModelAdmin):
    inlines = [HotelLogoInline,HouseInline]
    search_fields = ('name',)


class HotelImgAdmin(ModelAdmin):
    pass

class HouseAdmin(ModelAdmin):
    # inlines = [HousePackageInline,]
    list_display = ('hotel', 'name','checked','active',)
    fields = ('hotel', 'name', 'checked', 'active')
    search_fields = ('hotel__name','active')


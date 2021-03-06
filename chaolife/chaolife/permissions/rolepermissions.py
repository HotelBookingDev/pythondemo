#-*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission
from chaolife.models.orders import Order

# todo 使用全局的配置方式，不然修改不方便
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

ROLE_CUSTOMER = 1
PARTNER_CUSTOMER = 2


class PartnerPermission(BasePermission):
    """
        A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return  request.user.role == 2 or request.user.is_admin


    def has_object_permission(self, request, view, order):
        """
        Return `True` if permission is granted, `False` otherwise.
        admin is God!
        """
        return order.seller == request.user or request.user.is_admin


class IsHotelPartnerRole(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous():
            return False
        return request.user.is_partner_member


class CustomerPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_anonymous():
            return False
        return request.user.is_customer_member or request.user.is_admin


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated()
        )

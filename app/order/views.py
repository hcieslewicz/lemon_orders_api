from rest_framework import viewsets, mixins
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

from core.models import Stock, Order

from order import serializers


class OrderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Manage orders in the database"""
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    @staticmethod
    def _params_to_ints(qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

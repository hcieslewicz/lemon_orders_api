from rest_framework import serializers

from core.models import Stock, Order


def positive_number(value):
    if value <= 0:
        raise serializers.ValidationError('Value should be bigger than 0')


def max_length(value, max_length_value):
    if len(value) > max_length_value:
        raise serializers.ValidationError('Value should not be longer than %s' % max_length_value)


class StockSerializer(serializers.ModelSerializer):
    """Serializer for stock objects"""

    class Meta:
        model = Stock
        fields = ('id', 'isin', 'name')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Serialize an order"""
    @staticmethod
    def validate_isin(value):
        if len(value) > 12:
            raise serializers.ValidationError('ISIN is too long')
        return value

    @staticmethod
    def validate_limit_price(value):
        if value <= 0.00:
            raise serializers.ValidationError('Limit price should not be less than 0')
        return value

    @staticmethod
    def validate_side(value):
        v = value.lower()
        if v not in ['buy', 'sell']:
            raise serializers.ValidationError('Order action can be only "buy" or "sell"')
        return v

    @staticmethod
    def validate_valid_until(value):
        if value < 0:
            raise serializers.ValidationError('Order execution date before 1970 does not make any sense')
        return value

    @staticmethod
    def validate_quantity(value):
        if value <= 0:
            raise serializers.ValidationError('Quantity less or equal 0')
        return value

    class Meta:
        model = Order
        fields = (
            'id', 'isin', 'limit_price', 'side', 'valid_until', 'quantity'
        )
        read_only_fields = ('id',)

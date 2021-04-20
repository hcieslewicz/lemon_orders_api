from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Order, Stock


ORDERS_URL = reverse('order:order-list')


def sample_stock(name="Deutsche Wohnen SE", isin="DE000A0HN5C6", symbol="DWNI"):
    """Create and return a sample stock"""
    return Stock.objects.create(name=name, isin=isin, symbol=symbol)


class PublicOrderApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PrivateOrderpiTests(TestCase):
    """Test unauthenticated order API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@lemon.markets',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_create_order_successful(self):
        """Test creating a successful"""

        stock = sample_stock()

        payload = {
            'isin': stock.isin,
            'limit_price': 60.00,
            'side': 'buy',
            'valid_until': 1621518132,
            'quantity': 8
        }

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(order, key))

    def test_create_order_price_invalid_zero(self):
        stock = sample_stock()
        payload = {
            'isin': stock.isin,
            'limit_price': 0.00,
            'side': 'buy',
            'valid_until': 1621518132,
            'quantity': 8
        }

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_price_invalid_negative(self):
        stock = sample_stock()
        payload = {
            'isin': stock.isin,
            'limit_price': -10.50,
            'side': 'buy',
            'valid_until': 1621518132,
            'quantity': 4
        }

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_side_invalid(self):
        stock = sample_stock()
        payload = {
            'isin': stock.isin,
            'limit_price': 45.89,
            'side': 's',
            'valid_until': 1621518132,
            'quantity': 4
        }

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_side_capital(self):
        stock = sample_stock()
        payload = {
            'isin': stock.isin,
            'limit_price': 45.89,
            'side': '',
            'valid_until': 1621518132,
            'quantity': 4
        }

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

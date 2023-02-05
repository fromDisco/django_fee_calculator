# import python libraries
import json

# import django modules/libraries
from django.test import TestCase
from django.http import JsonResponse
from django.urls import reverse

# import app modules
from .views import CalculateFee


class TestCalculate(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.calculator = CalculateFee()

    def test_min_cart_val_fee(self):
        test_vals = [
            {
                "cart_value": 790,
                "expected": 210,
            },
            {
                "cart_value": 1000,
                "expected": 0,
            },
            {
                "cart_value": 999,
                "expected": 1,
            },
            {
                "cart_value": 1500,
                "expected": 0,
            },
        ]
        for vals in test_vals:
            cart_value = vals.get("cart_value")
            expected = vals.get("expected")
            result = self.calculator.min_cart_val_fee(cart_value)
            self.assertEqual(expected, result)

    def test_basic_fee(self):
        expected = 200
        result = self.calculator.basic_fee()
        self.assertEqual(expected, result)

    def test_distance_fee(self):
        test_vals = [
            {
                "delivery_distance": 499,
                "expected": 0,
            },
            {
                "delivery_distance": 1499,
                "expected": 100,
            },
            {
                "delivery_distance": 1500,
                "expected": 100,
            },
            {
                "delivery_distance": 1501,
                "expected": 200,
            },
        ]
        for vals in test_vals:
            delivery_distance = vals.get("delivery_distance")
            expected = vals.get("expected")
            result = self.calculator.distance_fee(delivery_distance)
            self.assertEqual(expected, result)

    def test_amount_fee(self):
        test_vals = [
            {
                "number_of_items": 4,
                "expected": 0,
            },
            {
                "number_of_items": 5,
                "expected": 50,
            },
            {
                "number_of_items": 10,
                "expected": 300,
            },
            {
                "number_of_items": 13,
                "expected": 450,
            },
        ]
        for vals in test_vals:
            number_of_items = vals.get("number_of_items")
            expected = vals.get("expected")
            result = self.calculator.amount_fee(number_of_items)
            self.assertEqual(expected, result)

    def test_bulk(self):
        test_vals = [
            {
                "number_of_items": 4,
                "expected": 0,
            },
            {
                "number_of_items": 12,
                "expected": 0,
            },
            {
                "number_of_items": 13,
                "expected": 120,
            },
        ]
        for vals in test_vals:
            number_of_items = vals.get("number_of_items")
            expected = vals.get("expected")
            result = self.calculator.bulk(number_of_items)
            self.assertEqual(expected, result)

    def test_delivery_fee_multiplier(self):
        test_vals = [
            {
                "order_time": "2021-10-12T13:00:00Z",
                "expected": 1.0,
            },
            {
                "order_time": "2023-02-03T14:59:00Z",
                "expected": 1.0,
            },
            {
                "order_time": "2023-02-03T15:00:00Z",
                "expected": 1.2,
            },
            {
                "order_time": "2023-02-03T19:00:00Z",
                "expected": 1.2,
            },
            {
                "order_time": "2023-02-03T19:01:00Z",
                "expected": 1.0,
            },
        ]
        for vals in test_vals:
            number_of_items = vals.get("order_time")
            expected = vals.get("expected")
            result = self.calculator.delivery_fee_multiplier(number_of_items)
            self.assertEqual(expected, result)

    def test_CalculateFee(self):
        test_vals = [
            {
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
                "expected": 710,
            },
            {
                "cart_value": 790,
                "delivery_distance": 500,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
                "expected": 410,
            },
            {
                "cart_value": 1000,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
                "expected": 500,
            },
            {
                "cart_value": 1000,
                "delivery_distance": 2235,
                "number_of_items": 5,
                "time": "2021-10-12T13:00:00Z",
                "expected": 550,
            },
            {
                "cart_value": 1000,
                "delivery_distance": 2235,
                "number_of_items": 13,
                "time": "2021-10-12T13:00:00Z",
                "expected": 1070,
            },
            {
                "cart_value": 10000,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2021-10-12T13:00:00Z",
                "expected": 0,
            },
            {
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2023-02-03T15:00:00Z",
                "expected": 852,
            },
        ]
        for vals in test_vals:

            dictionary = {
                "cart_value": vals.get("cart_value"),
                "delivery_distance": vals.get("delivery_distance"),
                "number_of_items": vals.get("number_of_items"),
                "time": vals.get("time"),
            }

            json_dict = json.dumps(dictionary)

            response = self.client.post(
                "/delivery_fee/", content_type="application/json", data=json_dict
            )

            # Test if connection is working
            self.assertEqual(response.status_code, 200)

            expected = vals.get("expected")
            # parse dict from json
            result = json.loads(response.content)
            self.assertEqual(expected, result.get("data"))

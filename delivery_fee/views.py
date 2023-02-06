# import python modules/libraries
import json
import datetime
import math
import dateutil.parser

# import django modules/libraries
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

# import app modules
from .models import FeeCalcVals


class CalculateFee(View):
    # get instance of default fee calculation values
    values = FeeCalcVals.objects.get(id=1)
    # declare fee calculation attributes
    cart_value_min = values.cart_value_min
    cart_value_max = values.cart_value_max
    distance_basic_fee = values.distance_basic_fee
    base_distance = values.base_distance
    distance_interval = values.distance_interval
    distance_interval_fee = values.distance_interval_fee
    item_amount_start = values.item_amount_start
    item_amount_fee = values.item_amount_fee
    bulk_number = values.bulk_number
    bulk_fee = values.bulk_fee
    delivery_fee_max = values.delivery_fee_max

    def min_cart_val_fee(self, cart_value: int) -> int:
        """
        If the cart_value is below a certain threshold,
        add the differnce between cart_value and threshold value
        """
        if cart_value < self.cart_value_min:
            return self.cart_value_min - cart_value
        return 0

    def basic_fee(self) -> int:
        """
        Return the basic distance fee
        """
        return self.distance_basic_fee

    def distance_fee(self, delivery_distance: int) -> int:
        """
        Return the distance fee, resulting from distance - base_distance, if delivery_distance is > then base_distance
        """
        if delivery_distance >= self.base_distance:
            return (
                math.ceil(
                    (delivery_distance - self.base_distance) / self.distance_interval
                )
                * self.distance_interval_fee
            )
        return 0

    def amount_fee(self, number_of_items: int) -> int:
        """
        From a threshold of items, add surcharge per item
        from this threshold.
        """
        if number_of_items >= self.item_amount_start:
            return (number_of_items - self.item_amount_start + 1) * self.item_amount_fee
        return 0

    def bulk(self, number_of_items: int) -> int:
        """
        From a certain number of items, add a bulk charge
        """
        if number_of_items > self.bulk_number:
            return self.bulk_fee
        return 0

    def delivery_fee_multiplier(self, order_time: str) -> float:
        """
        Set multiplier accordingly to order time

        arguments:
        order_time -- time string in ISO 8601
        """
        # convert iso-time-string to datetime object
        now = dateutil.parser.isoparse(order_time)

        min_hour = datetime.time(15, 00)
        max_hour = datetime.time(19, 00)

        if now.isoweekday() == 5 and min_hour <= now.time() <= max_hour:
            return 1.2

        return 1.0

    def post(self, request) -> JsonResponse:
        # read the incoming request data
        json_data = json.loads(request.body)

        # declare variables with json data
        cart_value = json_data.get("cart_value")
        delivery_distance = json_data.get("delivery_distance")
        number_of_items = json_data.get("number_of_items")
        order_time = json_data.get("time")

        # if cart_value > cart_value_max delivery_fee is 0 Euro
        # and exit calculation
        if cart_value >= self.cart_value_max:
            return JsonResponse({"delivery_fee": 0})

        delivery_fee = 0
        delivery_fee += self.min_cart_val_fee(cart_value)
        delivery_fee += self.basic_fee()
        delivery_fee += self.distance_fee(delivery_distance)
        delivery_fee += self.amount_fee(number_of_items)
        delivery_fee += self.bulk(number_of_items)

        delivery_fee_multiplier = self.delivery_fee_multiplier(order_time)
        delivery_fee *= delivery_fee_multiplier

        # set maximum value of delivery_fee
        if delivery_fee > self.delivery_fee_max:
            delivery_fee = self.delivery_fee_max

        return JsonResponse({"delivery_fee": int(delivery_fee)})

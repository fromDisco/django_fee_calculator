# import python modules/libraries
import json
import datetime
import math

# import django modules/libraries
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# import app modules
from .helpers import get_delivery_fee_multiplier
from .models import FeeCalcVals


@csrf_exempt
def calculate_fee(request):
    if request.method == "POST":
        # read the incoming request data
        json_data = json.loads(request.body)

        # declare variables with json data
        cart_value = json_data.get("cart_value")
        delivery_distance = json_data.get("delivery_distance")
        number_of_items = json_data.get("number_of_items")
        order_time = json_data.get("time")
        
        # get instance of default fee calculation values
        values = FeeCalcVals.objects.get(id=1)
        # declare fee calculation variables
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

        # declare start value of delivery_fee
        delivery_fee = 0

        # if cart_value > cart_value_max delivery_fee is 0 Euro!
        if cart_value >= cart_value_max:
            return JsonResponse({"delivery_fee": 0})

        # get the mulitplier for the delivery_fee
        # during rush hours multiply fee by x
        delivery_fee_multiplier = get_delivery_fee_multiplier(order_time)

        # when cart_value < cart_value_min, 
        # add the difference to the MIN_CART_VAL to fee
        if cart_value < cart_value_min:
            delivery_fee += cart_value_min - cart_value

        # delivery_fee += 200 for first 1000m 
        delivery_fee += distance_basic_fee

        # delivery_fee += (deliver_distance - 1000) / 500 * 100
        delivery_fee += math.ceil((delivery_distance - base_distance) / distance_interval) * distance_interval_fee
        
        # when number_of_items >= 5, add addidional x cents surcharge
        # per item starting starting from x items
        if number_of_items >= item_amount_start:
            delivery_fee += (number_of_items - item_amount_start + 1) * item_amount_fee

        # when number_of_items > 12, add x to delivery_fee
        if number_of_items > bulk_number:
            delivery_fee += bulk_fee

        delivery_fee *= delivery_fee_multiplier

        # set maximum amount of delivery_fee
        if delivery_fee > delivery_fee_max:
            delivery_fee = delivery_fee_max

        return JsonResponse({"data": int(delivery_fee)})
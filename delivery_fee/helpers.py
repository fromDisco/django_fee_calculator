# import python modules/libraries
import dateutil.parser
import datetime

# if 7pm UTC < time < 3pm UTC: delivery_muliplier = 1.2
# delivery_fee_multiplier = 1
# def get_delivery_fee_multiplier(order_time: str) -> float:
#    """Set multiplier accordingly to order time
#
#    arguments:
#    order_time -- time string in ISO 8601
#
#    return values:
#    multiplier -- multiplier, dependent on order time
#    """
#    # convert iso-time-string to datetime object
#    now = dateutil.parser.isoparse(order_time)
#
#    min_hour = datetime.time(15, 00)
#    max_hour = datetime.time(19, 00)
#
#    if now.isoweekday() == 5 and min_hour <= now.time() <= max_hour:
#        return 1.2
#
#    return 1.0
#

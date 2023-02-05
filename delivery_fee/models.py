from django.db import models

# Create your models here.
class FeeCalcVals(models.Model):
    cart_value_min = models.IntegerField()
    cart_value_max = models.IntegerField()
    distance_basic_fee = models.IntegerField()
    base_distance = models.IntegerField()
    distance_interval = models.IntegerField()
    distance_interval_fee = models.IntegerField()
    item_amount_start = models.IntegerField()
    item_amount_fee = models.IntegerField()
    bulk_number = models.IntegerField()
    bulk_fee = models.IntegerField()
    delivery_fee_max = models.IntegerField()

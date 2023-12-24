'''This module contain various models for database'''
from email.policy import default
from django.db import models, transaction
from django.db.models import F,Avg, ExpressionWrapper, fields
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    '''Model representing a vendor.'''
    name = models.CharField(max_length=30)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(unique=True,max_length=100)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    objects = models.Manager()

    def calculate_on_time_delivery_rate(self):
        '''Calculate on-time delivery rate.'''
        completed_purchases = self.purchase_orders
        on_time_deliveries = completed_purchases.filter(
           status='completed'
        )
        total_completed_purchases = completed_purchases.count()
        on_time_deliveries_count = on_time_deliveries.count()

        if total_completed_purchases > 0:
            on_time_delivery_rate = on_time_deliveries_count \
                                                / total_completed_purchases
            self.on_time_delivery_rate = on_time_delivery_rate*100
            self.save()

    def calculate_avg_quality_rating(self):
        '''Calculate average quality rating.'''
        completed_purchases = self.purchase_orders.filter(
            status='completed'
        ).exclude(quality_rating__isnull=True)
        
        if completed_purchases.exists():
            quality_rating_avg = completed_purchases.aggregate(
                Avg('quality_rating')
                )['quality_rating__avg']
        
        if quality_rating_avg is not None:
            self.quality_rating = quality_rating_avg
            self.save()
    
    def calculate_avg_response_time(self):
        '''Calculate average response time.'''
        completed_purchases = self.purchase_orders.filter(
            status='completed',acknowledgement_date__isnull=False
        )
        response_times = completed_purchases.annotate(
            response_time=ExpressionWrapper(
                F('acknowledgement_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        ).aggregate(Avg('response_time'))['response_time__avg']

        if response_times is not None:
            self.average_response_time = response_times.total_seconds()
            self.save()

    def calculate_fulfillment_rate(self):
        '''Calculate fulfillment rate.'''
        total_purchase = self.purchase_orders.count()
        fulfilled_purchases = self.purchase_orders.filter(
            status='completed',issue_date__isnull=False,
            acknowledgement_date__isnull=False
        )
        fulfilled_purchases_count = fulfilled_purchases.count()

        if total_purchase > 0:
            fulfillment_rate = fulfilled_purchases_count / total_purchase
            self.fulfillment_rate = fulfillment_rate*100
            self.save()
        

class PurchaseOrder(models.Model):
    '''Model representing a purchase order.'''
    po_number = models.CharField(unique=True,max_length=30)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=30)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True)

    objects = models.Manager()
    
class HistoricalPerfomance(models.Model):
    '''Model representing historical performance.'''
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name='historical_perfomances')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    objects = models.Manager()

@receiver(post_save,sender=PurchaseOrder)
def update_vendor_metrics(instance,**Kwargs):
    '''Update vendor metrics.'''
    vendor = instance.vendor

    #update the metrics upon acknowledgement of each PO
    if instance.acknowledgement_date is not None:
        vendor.calculate_avg_response_time()

    #Update the metrics upon completion each PO with qaulity_rating    
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor.calculate_avg_quality_rating()
    
    #Update the metrics upon change in PO status
    if instance.status == 'completed':
        vendor.calculate_on_time_delivery_rate()

    #Update the metrics upon any change in PO
    vendor.calculate_fulfillment_rate()

    #update the Historical perfomance within a transaction
    with transaction.atomic():
        HistoricalPerfomance.objects.create(
            vendor=vendor,
            date=instance.delivery_date,
            on_time_delivery_rate=vendor.on_time_delivery_rate,
            quality_rating_avg=vendor.quality_rating,
            average_response_time=vendor.average_response_time,
            fulfillment_rate=vendor.fulfillment_rate,
        )

'''module for maintaning serializers for models'''
from rest_framework import serializers
from . import models

class VendorCreateSerializer(serializers.ModelSerializer):
    '''serializer class for creation of vendor model object'''
    class Meta:
        model = models.Vendor
        fields = ['name','contact_details','address','vendor_code']

class VendorSerializer(serializers.ModelSerializer):
    '''serializer class for retrieving vendor model objects'''
    class Meta:
        model = models.Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    '''serializers class for Purchase order model'''
    class Meta:
        model = models.PurchaseOrder
        fields = '__all__'

class HistoricalPerfomanceSerializer(serializers.ModelSerializer):
    '''serializers class for historical perfomance'''
    class Meta:
        model = models.HistoricalPerfomance
        fields = ['on_time_delivery_rate','quality_rating_avg',
                  'average_response_time','fulfillment_rate']
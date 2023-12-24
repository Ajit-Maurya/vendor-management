'''this module contain class based views for API endpoints'''
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from . import models
from .serializers import VendorSerializer,PurchaseOrderSerializer
from .serializers import HistoricalPerfomanceSerializer,VendorCreateSerializer
# Create your views here.

class VendorListCreateView(generics.ListCreateAPIView):
    '''API endpoint to get list of vendors and
    create new vendor'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Vendor.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VendorCreateSerializer
        return VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''Endpoint for retrieving single vendor details,
    Update vendor details and delete a record of vendor'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class VendorPerformanceDetailView(generics.RetrieveAPIView):
    '''get perfomance detail of
    single vendor perfomance history'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.HistoricalPerfomance
    serializer_class = HistoricalPerfomanceSerializer

class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    '''get List of all purchase orders for a vendor with an
    option to filter by query parameter with value 'vendor'.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor',None)
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''retrieve single purchase order details,
    Update purcahse order details and delete a record of purchase order'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class AcknowledgePurchaseOrderView(generics.UpdateAPIView):
    '''provide functionality for vendor to
        acknowledge Purchase order'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        instance.acknowledgement_date = serializer.validated_data.get('acknowledgement_date')
        instance.save()

        vendor = instance.vendor
        vendor.calculate_avg_response_time()

        return Response(serializer.data,status=status.HTTP_200_OK)
    
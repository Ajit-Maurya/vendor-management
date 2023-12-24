'''module for url routing'''
from django.urls import path
from . import views


urlpatterns = [
    path('vendors',views.VendorListCreateView.as_view()),
    path('vendors/<int:pk>',views.VendorDetailView.as_view()),
    path('vendors/<int:pk>/performance',views.VendorPerformanceDetailView.as_view()),
    path('purchase_orders',views.PurchaseOrderListCreateView.as_view()),
    path('purchase_orders/<int:pk>',views.PurchaseOrderDetailView.as_view()),
    path('purchase_orders/<int:pk>/acknowledge',views.AcknowledgePurchaseOrderView.as_view()),
]
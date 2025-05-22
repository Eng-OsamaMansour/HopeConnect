from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from accounts.permissions import IsAdmin, IsLogistics, IsDonor
from logistics.serializers import DeliverySerializer
from .models import Delivery, Location, DeliveryStatus

# POST /api/deliveries/create/
class DeliveryCreateView(generics.CreateAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        # Create pickup location
        pickup_data = request.data.pop('pickup_location')
        pickup_location = Location.objects.create(**pickup_data)

        # Create dropoff location 
        dropoff_data = request.data.pop('dropoff_location')
        dropoff_location = Location.objects.create(**dropoff_data)

        # Create delivery with locations
        delivery_data = request.data
        delivery_data['pickup_location'] = pickup_location.id
        delivery_data['dropoff_location'] = dropoff_location.id

        # Create current location
        current_location_data = request.data.pop('current_location')
        current_location = Location.objects.create(**current_location_data)
        delivery_data['current_location'] = current_location.id
        
        serializer = self.get_serializer(data=delivery_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data)

# GET /api/deliveries/
class DeliveryListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsAdmin | IsLogistics]
    queryset = Delivery.objects.all()

# GET /api/deliveries/donor/
class DonorDeliveryListView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.filter(donation__donor=self.request.user)

# PATCH /api/deliveries/<pk>/status/
class DeliveryStatusUpdateView(generics.UpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAdmin | IsLogistics]

    def update(self, request, *args, **kwargs):
        delivery = self.get_object()
        status = request.data.get('status')
        
        if status not in DeliveryStatus.values:
            return Response(
                {"error": f"Invalid status. Must be one of: {DeliveryStatus.values}"}, 
                status=400
            )
            
        delivery.status = status
        delivery.save()
        return Response(self.get_serializer(delivery).data)

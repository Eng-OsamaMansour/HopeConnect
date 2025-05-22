from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from accounts.permissions import IsDonor, OrphanageOrAdminPermission

from .models import (
    Donation, DonationReport, GeneralDonation, EducationDonation,
    MedicalDonation, MoneyDonation, DonationType
)
from .serializers import (
    DonationReportSerializer, DonationSerializer, GeneralDonationSerializer,
    EducationDonationSerializer, MedicalDonationSerializer,
    MoneyDonationSerializer
)
from orphanages.models import Orphan


# POST /api/donations/general/
class GeneralDonationCreateView(generics.CreateAPIView):
    serializer_class = GeneralDonationSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data.get('donation_type') == DonationType.ORPHAN:
            if self.request.data.get('campaign'):
                raise ValidationError("Campaign should be empty for orphan donations")
        else:
            if self.request.data.get('orphan'):
                raise ValidationError("Orphan should be empty for campaign donations")
        
        serializer.save(donor=self.request.user)


# POST /api/donations/education/
class EducationDonationCreateView(generics.CreateAPIView):
    serializer_class = EducationDonationSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data.get('donation_type') == DonationType.ORPHAN:
            if self.request.data.get('campaign'):
                raise ValidationError("Campaign should be empty for orphan donations")
        else:
            if self.request.data.get('orphan'):
                raise ValidationError("Orphan should be empty for campaign donations")
        
        serializer.save(donor=self.request.user)


# POST /api/donations/medical/
class MedicalDonationCreateView(generics.CreateAPIView):
    serializer_class = MedicalDonationSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data.get('donation_type') == DonationType.ORPHAN:
            if self.request.data.get('campaign'):
                raise ValidationError("Campaign should be empty for orphan donations")
        else:
            if self.request.data.get('orphan'):
                raise ValidationError("Orphan should be empty for campaign donations")
        
        serializer.save(donor=self.request.user)


# POST /api/donations/money/
class MoneyDonationCreateView(generics.CreateAPIView):
    serializer_class = MoneyDonationSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.data.get('donation_type') == DonationType.ORPHAN:
            if self.request.data.get('campaign'):
                raise ValidationError("Campaign should be empty for orphan donations")
        else:
            if self.request.data.get('orphan'):
                raise ValidationError("Orphan should be empty for campaign donations")
        
        serializer.save(donor=self.request.user)


# GET /api/donations/donor/
class DonorDonationsListView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user)

# GET /api/donations/orphan/<orphan_id>/
class OrphanDonationsListView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [OrphanageOrAdminPermission]

    def get_queryset(self):
        orphan = get_object_or_404(Orphan, id=self.kwargs['orphan_id'])
        self.check_object_permissions(self.request, orphan)
        return Donation.objects.filter(orphan=orphan)


# POST /api/donations/<pk>/report/
class DonationReportCreateView(generics.CreateAPIView):
    serializer_class = DonationReportSerializer
    permission_classes = [OrphanageOrAdminPermission]

    def perform_create(self, serializer):
        donation = get_object_or_404(Donation, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, donation)
        serializer.save(donation=donation)


# GET /api/donations/<pk>/report/
class DonationReportListView(generics.ListAPIView):
    serializer_class = DonationReportSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def get_queryset(self):
        donation = get_object_or_404(Donation, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, donation)
        return DonationReport.objects.filter(donation=donation)

# get reports for for a specific donor
# GET /api/donations/donor/reports/
class DonorReportsListView(generics.ListAPIView):
    serializer_class = DonationReportSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def get_queryset(self):
        return DonationReport.objects.filter(donation__donor=self.request.user)
    
# PATCH /api/donations/<pk>/status/
class DonationStatusUpdateView(generics.UpdateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        donation = self.get_object()
        donation.status = request.data.get('status')
        donation.save()
        return Response(self.get_serializer(donation).data)




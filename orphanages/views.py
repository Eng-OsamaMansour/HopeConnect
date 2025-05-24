from rest_framework import generics
from accounts.permissions import IsAdmin, IsDonor, IsOrphanage
from .models import Orphanage, OrphanageNeedRequest, Review
from .serializers import  OrphanageNeedRequestSerializer, ReviewSerializer, OrphanageSerializer
from rest_framework import  permissions
from .models import Orphanage

from django.db.models import Avg, Count




class OrphanageListView(generics.ListAPIView):
    queryset = Orphanage.objects.annotate(
        avg_rating=Avg('reviews__stars'),
        rating_count=Count('reviews')
    )
    serializer_class = OrphanageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']


# PUT/PATCH /api/orphanages/<id>/
# Updates orphanage details, restricted to admin or orphanage manager
class OrphanageUpdateView(generics.UpdateAPIView):
    queryset = Orphanage.objects.all()
    serializer_class = OrphanageSerializer
    permission_classes = [IsAdmin | IsOrphanage]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ORPHANAGE":
            return self.queryset.filter(manager=user)
        return self.queryset


# POST /api/orphanages/
# Creates new orphanage, admin only
class OrphanageCreateView(generics.CreateAPIView):
    serializer_class = OrphanageSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save()


# GET /api/orphanages/<id>/reviews/
# Lists all reviews for a specific orphanage
class OrphanageReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        orphanage_id = self.kwargs['pk']
        return Review.objects.filter(orphanage_id=orphanage_id)

# POST /api/orphanages/<id>/reviews/
# Creates a new review for an orphanage
class OrphanageReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsDonor]

    def get_queryset(self):
        return Review.objects.filter(orphanage=self.kwargs['pk'])
    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)


# POST /api/orphanages/<id>/verify/
# Upload verification documents for an orphanage
class OrphanageVerificationView(generics.UpdateAPIView):
    queryset = Orphanage.objects.all()
    serializer_class = OrphanageSerializer
    permission_classes = [IsOrphanage]

    def get_queryset(self):
        return self.queryset.filter(manager=self.request.user)


# POST /api/orphanages/need-requests/create/
# Creates a new need request for an orphanage
class OrphanageNeedRequestCreateView(generics.CreateAPIView):
    serializer_class = OrphanageNeedRequestSerializer
    permission_classes = [IsOrphanage]

    def perform_create(self, serializer):
        orphanage = Orphanage.objects.get(manager=self.request.user)
        serializer.save(orphanage=orphanage)

# GET /api/orphanages/need-requests/
# Lists all need requests for an orphanage
class OrphanageNeedRequestListView(generics.ListAPIView):
    serializer_class = OrphanageNeedRequestSerializer
    permission_classes = [IsOrphanage]

    def get_queryset(self):
        return OrphanageNeedRequest.objects.filter(orphanage=Orphanage.objects.get(manager=self.request.user))

# GET /api/orphanages/need-requests/list/
# Lists all need requests for all orphanages
class OrphanageNeedRequestListView(generics.ListAPIView):
    serializer_class = OrphanageNeedRequestSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return OrphanageNeedRequest.objects.all()

# PATCH /api/orphanages/need-requests/<id>/
# Closes a need request
class OrphanageNeedRequestUpdateView(generics.UpdateAPIView):
    serializer_class = OrphanageNeedRequestSerializer
    permission_classes = [IsOrphanage]

    def get_queryset(self):
        return OrphanageNeedRequest.objects.filter(orphanage=Orphanage.objects.get(manager=self.request.user))  
    def perform_update(self, serializer):
        serializer.save(is_open=False)  




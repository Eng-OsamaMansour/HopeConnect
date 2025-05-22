from rest_framework import viewsets,generics
from accounts.permissions import IsAdmin, IsDonor, IsOrphanage
from .models import Orphan, Orphanage, Review
from .serializers import OrphanSerializer, OrphanageSerializer, OrphanageVerifySerializer, ReviewSerializer
from rest_framework import mixins, viewsets, permissions
from .models import Orphanage
from .serializers import OrphanageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count




class OrphanageListView(generics.ListAPIView):
    queryset = Orphanage.objects.annotate(
        avg_rating=Avg('review__stars'),
        rating_count=Count('review')
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
    queryset = Orphanage.objects.all()
    serializer_class = OrphanageSerializer
    permission_classes = [IsAdmin]


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
    serializer_class = OrphanageVerifySerializer
    permission_classes = [IsOrphanage]

    def get_queryset(self):
        return self.queryset.filter(manager=self.request.user)



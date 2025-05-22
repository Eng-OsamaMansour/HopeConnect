from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Orphan, OrphanUpdate, OrphanSponsor
from orphanages.models import Orphanage
from .serializers import OrphanSerializer, OrphanUpdateSerializer, OrphanSponsorSerializer
from accounts.permissions import IsAdmin, IsOrphanage, IsDonor, OrphanageOrAdminPermission

# POST /api/orphans/
class OrphanCreateView(generics.CreateAPIView):
    serializer_class = OrphanSerializer
    permission_classes = [IsAdmin | IsOrphanage]

    def perform_create(self, serializer):
        if not Orphanage.objects.get(manager=self.request.user).is_public_approved:
            raise ValidationError("Your orphanage is not approved yet")
        if self.request.user.role == 'ORPHANAGE':
            serializer.save(orphanage=Orphanage.objects.get(manager=self.request.user))
        else:
            serializer.save()

# POST /api/orphans/<orphan_id>/updates/
class OrphanUpdateCreateView(generics.CreateAPIView):
    serializer_class = OrphanUpdateSerializer
    permission_classes = [OrphanageOrAdminPermission]

    def perform_create(self, serializer):
        if not Orphanage.objects.get(manager=self.request.user).is_public_approved:
            raise ValidationError("Your orphanage is not approved yet")
        orphan = get_object_or_404(Orphan, id=self.kwargs['orphan_id'])
        self.check_object_permissions(self.request, orphan)
        serializer.save(orphan=orphan)

# GET /api/orphans/<orphan_id>/updates/
class OrphanUpdateListView(generics.ListAPIView):
    serializer_class = OrphanUpdateSerializer
    permission_classes = [permissions.IsAuthenticated &  (IsOrphanage | IsAdmin | IsDonor)]
    def get_queryset(self):
        if self.request.user.role == 'ORPHANAGE':
            if not Orphanage.objects.get(manager=self.request.user).is_public_approved:
                raise ValidationError("Your orphanage is not approved yet")
        orphan = get_object_or_404(Orphan, id=self.kwargs['orphan_id']) 
        return OrphanUpdate.objects.filter(orphan=orphan)

# POST /api/orphans/<orphan_id>/sponsor/
class OrphanSponsorCreateView(generics.CreateAPIView):
    serializer_class = OrphanSponsorSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        orphan = get_object_or_404(Orphan, id=self.kwargs['orphan_id'])
        serializer.save(donor=self.request.user, orphan=orphan)

# PATCH /api/orphans/sponsors/<pk>/cancel/
class OrphanSponsorCancelView(generics.UpdateAPIView):
    queryset = OrphanSponsor.objects.all()
    serializer_class = OrphanSponsorSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_update(self, serializer):
        sponsor = self.get_object()
        if sponsor.donor != self.request.user:
            raise ValidationError("You can only cancel your own sponsorships")
        serializer.save(is_active=False)

# DELETE /api/orphans/<pk>/
class OrphanDestroyView(generics.DestroyAPIView):
    queryset = Orphan.objects.all()
    serializer_class = OrphanSerializer
    permission_classes = [OrphanageOrAdminPermission]

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()
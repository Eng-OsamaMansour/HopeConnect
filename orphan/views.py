from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Orphan, OrphanUpdate, OrphanSponsor
from orphanages.models import Orphanage
from .serializers import OrphanSerializer, OrphanUpdateSerializer, OrphanSponsorSerializer
from accounts.permissions import IsAdmin, IsOrphanage, IsDonor, OrphanageOrAdminPermission
from rest_framework import status

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

# POST /api/orphans/sponsor/
class OrphanSponsorCreateView(generics.CreateAPIView):
    serializer_class = OrphanSponsorSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def perform_create(self, serializer):
        orphan = get_object_or_404(Orphan, id=self.request.data.get('orphan'))
        serializer.save(donor=self.request.user, orphan=orphan)

# PATCH /api/orphans/sponsor/cancel/
class OrphanSponsorCancelView(generics.GenericAPIView):
    serializer_class = OrphanSponsorSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        orphan_id = self.request.data.get("orphan")
        sponsor = OrphanSponsor.objects.filter(donor=self.request.user, orphan_id=orphan_id).first()
        if not sponsor:
            raise ValidationError("You are not sponsoring this orphan.")
        sponsor.is_active = False
        sponsor.save()
        serializer = self.get_serializer(sponsor)
        return Response(data=serializer.data, status=200)


    
# GET /api/orphans/sponsors/
class OrphanSponsorListView(generics.ListAPIView):
    serializer_class = OrphanSponsorSerializer
    permission_classes = [IsDonor & permissions.IsAuthenticated]
    def get_queryset(self):
        return OrphanSponsor.objects.filter(donor=self.request.user , is_active=True)
    
# DELETE /api/orphans/<pk>/
class OrphanDestroyView(generics.DestroyAPIView):
    queryset = Orphan.objects.all()
    serializer_class = OrphanSerializer
    permission_classes = [OrphanageOrAdminPermission]

    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        instance.delete()
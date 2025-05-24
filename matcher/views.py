from rest_framework import generics

from accounts.models import Role
from orphanages.models import Orphanage
from .models import Matcher
from .serializers import MatcherSerializer
from accounts.permissions import IsAdmin, IsOrphanage, IsVolunteer
from django.db.models import Q

# GET /api/matcher/

class MatcherView(generics.ListAPIView):
    serializer_class = MatcherSerializer
    permission_classes = [IsAdmin | IsOrphanage | IsVolunteer]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.VOLUNTEER:
            return Matcher.objects.filter(volunteer_offer__volunteer=user)
        elif user.role == Role.ORPHANAGE:
            orphanage = Orphanage.objects.get(manager=user)
            return Matcher.objects.filter(need_request__orphanage=orphanage)
        return Matcher.objects.none()

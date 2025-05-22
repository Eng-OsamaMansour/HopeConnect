from rest_framework import generics
from .models import Matcher
from .serializers import MatcherSerializer
from accounts.permissions import IsAdmin, IsOrphanage, IsVolunteer
from django.db.models import Q

# GET /api/matcher/
class MatcherView(generics.ListAPIView):
    serializer_class = MatcherSerializer
    permission_classes = [IsAdmin | IsOrphanage | IsVolunteer]

    def get_queryset(self):
        return Matcher.objects.filter(
            Q(volunteer_offer__volunteer=self.request.user) |
            Q(need_request__orphanage=self.request.user)
        )


from rest_framework import generics, permissions
from accounts.permissions import IsVolunteer, IsOrphanage, IsAdmin
from .models import Volunteer, VolunteerOfferRequest
from .serializers import VolunteerSerializer, VolunteerOfferRequestSerializer


# POST /api/volunteers/
# Creates new volunteer profile, restricted to users with volunteer role
class VolunteerCreateView(generics.CreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [IsVolunteer]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# PUT/PATCH /api/volunteers/<id>/
# Updates volunteer profile, restricted to profile owner
class VolunteerUpdateView(generics.UpdateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


# POST /api/volunteer-offers/
# Creates new volunteer offer request
class VolunteerOfferRequestCreateView(generics.CreateAPIView):
    queryset = VolunteerOfferRequest.objects.all()
    serializer_class = VolunteerOfferRequestSerializer
    permission_classes = [IsVolunteer]

    def perform_create(self, serializer):
        volunteer = self.request.user.volunteer
        serializer.save(volunteer=volunteer)


# PUT/PATCH /api/volunteer-offers/<id>/
# Updates volunteer offer request, restricted to offer owner
class VolunteerOfferRequestUpdateView(generics.UpdateAPIView):
    queryset = VolunteerOfferRequest.objects.all()
    serializer_class = VolunteerOfferRequestSerializer
    permission_classes = [IsVolunteer]

    def get_queryset(self):
        volunteer = self.request.user.volunteer
        return self.queryset.filter(volunteer=volunteer)


# GET /api/volunteer-offers/
# Lists all volunteer offers, filtered by user role
class VolunteerOfferRequestListView(generics.ListAPIView):
    serializer_class = VolunteerOfferRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = VolunteerOfferRequest.objects.all()

        # Admins and orphanages can see all requests
        if user.role in ['ADMIN', 'ORPHANAGE']:
            return queryset

        # Volunteers can only see their own requests
        if user.role == 'VOLUNTEER':
            return queryset.filter(volunteer__user=user)

        return VolunteerOfferRequest.objects.none()


# GET /api/volunteer-offers/my-requests/
# Lists volunteer's own requests
class MyVolunteerOfferRequestsView(generics.ListAPIView):
    serializer_class = VolunteerOfferRequestSerializer
    permission_classes = [IsVolunteer]

    def get_queryset(self):
        return VolunteerOfferRequest.objects.filter(volunteer__user=self.request.user)
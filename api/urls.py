# api/urls.py  – SINGLE source of truth
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from accounts.views     import RegisterViewSet, UserMeViewSet
from orphanages.views   import OrphanageViewSet, OrphanViewSet, ReviewViewSet
from donations.views    import DonationViewSet, OrphanSponsorViewSet
from volunteers.views   import VolunteerRequestViewSet
from logistics.views    import DeliveryViewSet
from payments.views import DonationPaymentIntentView
from volunteers.views import VolunteerMatchRunView
from impact.views import MyImpactView
from orphanages.views import PublicOrphanageViewSet
from  campaigns.views import EmergencyCampaignListView
from donations.views import CampaignLedgerView

\

router = DefaultRouter()

# auth
router.register("auth/register", RegisterViewSet, basename="auth-register")
router.register("auth/me",       UserMeViewSet,   basename="auth-me")

# domain
router.register("orphanages",        OrphanageViewSet,       basename="orphanage")  
router.register("orphans",           OrphanViewSet,          basename="orphan")
router.register("sponsorships",      OrphanSponsorViewSet,   basename="sponsorship")
router.register("donations",         DonationViewSet,        basename="donation")
router.register("volunteer-requests",VolunteerRequestViewSet,basename="volunteer-request")
router.register("deliveries",        DeliveryViewSet,        basename="delivery")
router.register("orphanages-public", PublicOrphanageViewSet, basename="orphanage-public")
router.register("reviews", ReviewViewSet, basename="review")


urlpatterns = [path("", include(router.urls))]
urlpatterns += [
    path("donations/<int:pk>/intent/", DonationPaymentIntentView.as_view(), name="donation-intent"),
    path("volunteer-match/", VolunteerMatchRunView.as_view(), name="volunteer-match"),
    path("my-impact/", MyImpactView.as_view(), name="my-impact"),
    path("campaigns/emergency/active/", EmergencyCampaignListView.as_view(),name="emergency-campaigns"),
    path("campaigns/<int:pk>/ledger/", CampaignLedgerView.as_view(),name="campaign-ledger"),

]


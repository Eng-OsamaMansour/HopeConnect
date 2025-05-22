from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payment import views as payment_views
from donations import views as donation_views
from logistics import views as logistics_views
from orphan import views as orphan_views
from orphanages import views as orphanage_views
from matcher import views as matcher_views
from volunteers import views as volunteer_views
from accounts import views

router = DefaultRouter()
router.register(r'payments', payment_views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # Auth URLs
    path('auth/login/', views.LoginView.as_view()),
    path('auth/logout/', views.LogoutView.as_view({'post': 'logout'})),
    path('users/', views.UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('users/<int:pk>/', views.UserViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'
    })),

    # Donations URLs
    path('donations/general/', donation_views.GeneralDonationCreateView.as_view()),
    path('donations/education/', donation_views.EducationDonationCreateView.as_view()),
    path('donations/medical/', donation_views.MedicalDonationCreateView.as_view()),
    path('donations/money/', donation_views.MoneyDonationCreateView.as_view()),
    path('donations/donor/', donation_views.DonorDonationsListView.as_view()),
    path('donations/orphan/<int:orphan_id>/', donation_views.OrphanDonationsListView.as_view()),
    path('donations/<int:pk>/report/', donation_views.DonationReportCreateView.as_view()),
    path('donations/<int:pk>/reports/', donation_views.DonationReportListView.as_view()),
    path('donations/donor/reports/', donation_views.DonorReportsListView.as_view()),
    path('donations/<int:pk>/status/', donation_views.DonationStatusUpdateView.as_view()),

    # Logistics URLs
    path('deliveries/create/', logistics_views.DeliveryCreateView.as_view()),
    path('deliveries/', logistics_views.DeliveryListView.as_view()),
    path('deliveries/donor/', logistics_views.DonorDeliveryListView.as_view()),
    path('deliveries/<int:pk>/status/', logistics_views.DeliveryStatusUpdateView.as_view()),

    # Orphan URLs
    path('orphans/', orphan_views.OrphanCreateView.as_view()),
    path('orphans/<int:orphan_id>/updates/', orphan_views.OrphanUpdateCreateView.as_view()),
    path('orphans/<int:orphan_id>/updates/list/', orphan_views.OrphanUpdateListView.as_view()),
    path('orphans/<int:orphan_id>/sponsor/', orphan_views.OrphanSponsorCreateView.as_view()),
    path('orphans/sponsors/<int:pk>/cancel/', orphan_views.OrphanSponsorCancelView.as_view()),
    path('orphans/<int:pk>/', orphan_views.OrphanDestroyView.as_view()),

    # Orphanage URLs
    path('orphanages/', orphanage_views.OrphanageListView.as_view()),
    path('orphanages/<int:pk>/', orphanage_views.OrphanageUpdateView.as_view()),
    path('orphanages/create/', orphanage_views.OrphanageCreateView.as_view()),
    path('orphanages/<int:pk>/reviews/', orphanage_views.OrphanageReviewsView.as_view()),
    path('orphanages/<int:pk>/reviews/create/', orphanage_views.OrphanageReviewCreateView.as_view()),
    path('orphanages/<int:pk>/verify/', orphanage_views.OrphanageVerificationView.as_view()),

    # Matcher URLs
    path('matcher/', matcher_views.MatcherView.as_view()),

    # Volunteer URLs
    path('volunteers/', volunteer_views.VolunteerCreateView.as_view()),
    path('volunteers/<int:pk>/', volunteer_views.VolunteerUpdateView.as_view()),
    path('volunteer-offers/', volunteer_views.VolunteerOfferRequestListView.as_view()),
    path('volunteer-offers/create/', volunteer_views.VolunteerOfferRequestCreateView.as_view()),
    path('volunteer-offers/<int:pk>/', volunteer_views.VolunteerOfferRequestUpdateView.as_view()),
    path('volunteer-offers/my-requests/', volunteer_views.MyVolunteerOfferRequestsView.as_view()),
]
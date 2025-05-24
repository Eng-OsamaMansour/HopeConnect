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
from campaigns import views as campaign_views
router = DefaultRouter()
router.register(r'payments', payment_views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    # Auth URLs
    path('auth/login/', views.LoginView.as_view()), #DONE
    path('auth/logout/', views.LogoutView.as_view({'post': 'logout'})), #DONE
    path('users/list/', views.UserListView.as_view()), #DONE
    path('users/create/', views.UserCreateView.as_view()), #DONE
    path('users/me/', views.UserDetailView.as_view()), #DONE
    path('users/me/update/', views.UserUpdateView.as_view()), #DONE
    path('users/me/delete/', views.UserDeleteView.as_view()), #DONE

    # Donations URLs
    path('donations/', donation_views.DonationCreateView.as_view()), #NOT USED
    path('donations/general/', donation_views.GeneralDonationCreateView.as_view()), #DONE
    path('donations/education/', donation_views.EducationDonationCreateView.as_view()), #DONE
    path('donations/medical/', donation_views.MedicalDonationCreateView.as_view()), #DONE
    path('donations/money/', donation_views.MoneyDonationCreateView.as_view()), #DONE
    path('donations/donor/', donation_views.DonorDonationsListView.as_view()), #DONE
    path('donations/orphan/<int:orphan_id>/', donation_views.OrphanDonationsListView.as_view()), #DONE
    path('donations/<int:pk>/report/', donation_views.DonationReportCreateView.as_view()), #DONE    
    path('donations/<int:pk>/reports/', donation_views.DonationReportListView.as_view()), #DONE
    path('donations/donor/reports/', donation_views.DonorReportsListView.as_view()), #DONE
    path('donations/<int:pk>/status/', donation_views.DonationStatusUpdateView.as_view()), #DONE

    # Logistics URLs
    path('deliveries/create/', logistics_views.DeliveryCreateView.as_view()), #DONE
    path('deliveries/', logistics_views.DeliveryListView.as_view()), #DONE
    path('deliveries/donor/', logistics_views.DonorDeliveryListView.as_view()), #DONE
    path('deliveries/<int:pk>/status/', logistics_views.DeliveryStatusUpdateView.as_view()), #DONE

    # Orphan URLs
    path('orphans/', orphan_views.OrphanCreateView.as_view()), #DONE
    path('orphans/<int:orphan_id>/updates/', orphan_views.OrphanUpdateCreateView.as_view()), #DONE
    path('orphans/<int:orphan_id>/updates/list/', orphan_views.OrphanUpdateListView.as_view()), #DONE
    path('orphans/<int:pk>/', orphan_views.OrphanDestroyView.as_view()), #NOT USED
    path('orphans/sponsor/', orphan_views.OrphanSponsorCreateView.as_view()), #DONE
    path('orphans/sponsor/cancel/', orphan_views.OrphanSponsorCancelView.as_view()), #DONE
    path('orphans/sponsors/', orphan_views.OrphanSponsorListView.as_view()), #DONE

    # Orphanage URLs
    path('orphanages/', orphanage_views.OrphanageListView.as_view()), #DONE
    path('orphanages/<int:pk>/', orphanage_views.OrphanageUpdateView.as_view()), #DONE
    path('orphanages/create/', orphanage_views.OrphanageCreateView.as_view()), #DONE
    path('orphanages/<int:pk>/reviews/', orphanage_views.OrphanageReviewsView.as_view()), #DONE
    path('orphanages/<int:pk>/reviews/create/', orphanage_views.OrphanageReviewCreateView.as_view()),#DONE
    path('orphanages/<int:pk>/verify/', orphanage_views.OrphanageVerificationView.as_view()), #DONE
    path('orphanages/need-requests/', orphanage_views.OrphanageNeedRequestListView.as_view()), #DONE
    path('orphanages/need-requests/create/', orphanage_views.OrphanageNeedRequestCreateView.as_view()), #DONE
    path('orphanages/need-requests/list/', orphanage_views.OrphanageNeedRequestListView.as_view()), #DONE
    path('orphanages/need-requests/<int:pk>/', orphanage_views.OrphanageNeedRequestUpdateView.as_view()), #DONE
    # Matcher URLs
    path('matcher/', matcher_views.MatcherView.as_view()), #DONE

    # Volunteer URLs
    path('volunteers/', volunteer_views.VolunteerCreateView.as_view()),
    path('volunteers/<int:pk>/', volunteer_views.VolunteerUpdateView.as_view()),

    path('volunteer-offers/', volunteer_views.VolunteerOfferRequestListView.as_view()),
    path('volunteer-offers/create/', volunteer_views.VolunteerOfferRequestCreateView.as_view()),
    path('volunteer-offers/<int:pk>/', volunteer_views.VolunteerOfferRequestUpdateView.as_view()),
    path('volunteer-offers/my-requests/', volunteer_views.MyVolunteerOfferRequestsView.as_view()),

    # Campaign URLs
    path('campaigns/', campaign_views.CampaignCreateView.as_view()),
    path('campaigns/<int:pk>/close/', campaign_views.CampaignCloseView.as_view()),
    path('campaigns/open/', campaign_views.OpenCampaignsListView.as_view()),
    path('campaigns/<int:pk>/donations/', campaign_views.CampaignDonationsListView.as_view()),
]
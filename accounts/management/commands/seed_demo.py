from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
import json
from decimal import Decimal
from faker import Faker
from accounts.models import User, Role
from orphanages.models import Orphanage, OrphanageNeedRequest, Review
from orphan.models import Orphan, OrphanGender, OrphanSponsor, OrphanUpdate
from donations.models import (
    Donation, DonationCategory, DonationStatus, DonationType,
    GeneralDonation, EducationDonation, MedicalDonation, MoneyDonation,
    DonationReport
)
from campaigns.models import Campaign, CampaignCategory
from logistics.models import Delivery, DeliveryStatus, Location
from volunteers.models import Volunteer, VolunteerOfferRequest, OfferStatus
from matcher.models import Matcher
import os

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **kwargs):
        # Set seeding flag
        os.environ['DJANGO_SEEDING'] = 'true'
        
        self.stdout.write('Creating demo data...')
        
        try:
            # Create users with different roles
            users_data = []
            users = self.create_users(users_data)
            
            # Create orphanages
            orphanages = self.create_orphanages(users['orphanage'])
            
            # Create orphans
            orphans = self.create_orphans(orphanages)
            
            # Create campaigns
            campaigns = self.create_campaigns()
            
            # Create donations
            donations = self.create_donations(users['donor'], orphans, campaigns)
            
            # Create delivery records
            deliveries = self.create_deliveries(donations, users['logistics'])
            
            # Create volunteers and their offers
            volunteers = self.create_volunteers(users['volunteer'])
            offers = self.create_volunteer_offers(volunteers)
            
            # Create need requests and matches
            need_requests = self.create_need_requests(orphanages)
            matches = self.create_matches(need_requests, offers)
            
            # Create reviews
            self.create_reviews(users['donor'], orphanages)
            
            # Create orphan sponsorships
            self.create_orphan_sponsorships(orphans, users['donor'])
            
            # Create orphan updates
            self.create_orphan_updates(orphans)
            
            # Save user credentials to a file
            self.save_user_credentials(users_data)
            
            self.stdout.write(self.style.SUCCESS('Successfully created demo data'))
        finally:
            # Reset seeding flag
            os.environ['DJANGO_SEEDING'] = 'false'

    def create_users(self, users_data):
        users = {
            'admin': [],
            'donor': [],
            'orphanage': [],
            'volunteer': [],
            'logistics': []
        }
        
        # Create admin users
        for i in range(2):
            user = User.objects.create_user(
                email=f'admin{i+1}@example.com',
                password='admin123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=Role.ADMIN,
                phone_number=fake.phone_number()
            )
            users['admin'].append(user)
            users_data.append({
                'email': user.email,
                'password': 'admin123',
                'role': 'ADMIN'
            })

        # Create donor users
        for i in range(10):
            user = User.objects.create_user(
                email=f'donor{i+1}@example.com',
                password='donor123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=Role.DONOR,
                phone_number=fake.phone_number()
            )
            users['donor'].append(user)
            users_data.append({
                'email': user.email,
                'password': 'donor123',
                'role': 'DONOR'
            })

        # Create orphanage users
        for i in range(5):
            user = User.objects.create_user(
                email=f'orphanage{i+1}@example.com',
                password='orphanage123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=Role.ORPHANAGE,
                phone_number=fake.phone_number()
            )
            users['orphanage'].append(user)
            users_data.append({
                'email': user.email,
                'password': 'orphanage123',
                'role': 'ORPHANAGE'
            })

        # Create volunteer users
        for i in range(8):
            user = User.objects.create_user(
                email=f'volunteer{i+1}@example.com',
                password='volunteer123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=Role.VOLUNTEER,
                phone_number=fake.phone_number()
            )
            users['volunteer'].append(user)
            users_data.append({
                'email': user.email,
                'password': 'volunteer123',
                'role': 'VOLUNTEER'
            })

        # Create logistics users
        for i in range(3):
            user = User.objects.create_user(
                email=f'logistics{i+1}@example.com',
                password='logistics123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=Role.LOGISTICS,
                phone_number=fake.phone_number()
            )
            users['logistics'].append(user)
            users_data.append({
                'email': user.email,
                'password': 'logistics123',
                'role': 'LOGISTICS'
            })

        return users

    def create_orphanages(self, orphanage_users):
        orphanages = []
        for user in orphanage_users:
            orphanage = Orphanage.objects.create(
                manager=user,
                name=fake.company(),
                city=fake.city(),
                latitude=Decimal(str(fake.latitude())),
                longitude=Decimal(str(fake.longitude())),
                is_public_approved=random.choice([True, False])
            )
            orphanages.append(orphanage)
        return orphanages

    def create_orphans(self, orphanages):
        orphans = []
        for orphanage in orphanages:
            for _ in range(random.randint(5, 15)):
                orphan = Orphan.objects.create(
                    orphanage=orphanage,
                    national_id=fake.unique.random_number(digits=14),
                    name=fake.name(),
                    gender=random.choice([OrphanGender.MALE, OrphanGender.FEMALE]),
                    birth_date=fake.date_of_birth(minimum_age=5, maximum_age=18),
                    health_info=fake.text(),
                    education_status=random.choice(['Primary', 'Secondary', 'High School'])
                )
                orphans.append(orphan)
        return orphans

    def create_campaigns(self):
        campaigns = []
        for _ in range(5):
            campaign = Campaign.objects.create(
                title=fake.catch_phrase(),
                category=random.choice([c[0] for c in CampaignCategory.choices]),
                goal_amount=Decimal(random.randint(1000, 10000)),
                start=timezone.now().date(),
                end=timezone.now().date() + timedelta(days=random.randint(30, 90)),
                is_open=True
            )
            campaigns.append(campaign)
        return campaigns

    def create_donations(self, donors, orphans, campaigns):
        donations = []
        
        # Create general donations
        for _ in range(20):
            donation = GeneralDonation.objects.create(
                donor=random.choice(donors),
                orphan=random.choice(orphans),
                campaign=random.choice(campaigns),
                description=fake.text(),
                material=random.choice(['Clothes', 'Books', 'Toys', 'Food']),
                quantity=random.randint(1, 10),
                need_transportation=random.choice([True, False]),
                status=random.choice([s[0] for s in DonationStatus.choices]),
                donation_type=random.choice([t[0] for t in DonationType.choices])
            )
            donations.append(donation)

        # Create education donations
        for _ in range(15):
            donation = EducationDonation.objects.create(
                donor=random.choice(donors),
                orphan=random.choice(orphans),
                campaign=random.choice(campaigns),
                field=random.choice(['Math', 'Science', 'English', 'Art']),
                course=random.choice(['Basic', 'Intermediate', 'Advanced']),
                course_duration=random.randint(1, 12),
                hours_per_week=random.randint(1, 5),
                status=random.choice([s[0] for s in DonationStatus.choices]),
                donation_type=random.choice([t[0] for t in DonationType.choices])
            )
            donations.append(donation)

        # Create medical donations
        for _ in range(10):
            donation = MedicalDonation.objects.create(
                donor=random.choice(donors),
                orphan=random.choice(orphans),
                campaign=random.choice(campaigns),
                supply_type=random.choice(['Medicine', 'Equipment', 'First Aid']),
                quantity=random.randint(1, 5),
                description=fake.text(),
                status=random.choice([s[0] for s in DonationStatus.choices]),
                donation_type=random.choice([t[0] for t in DonationType.choices])
            )
            donations.append(donation)

        # Create money donations
        for _ in range(25):
            donation = MoneyDonation.objects.create(
                donor=random.choice(donors),
                orphan=random.choice(orphans),
                campaign=random.choice(campaigns),
                amount=Decimal(random.randint(50, 1000)),
                pay_for=random.choice(['Education', 'Medical', 'Food', 'Clothing']),
                currency='USD',
                status=random.choice([s[0] for s in DonationStatus.choices]),
                donation_type=random.choice([t[0] for t in DonationType.choices])
            )
            donations.append(donation)

        return donations

    def create_deliveries(self, donations, logistics_users):
        deliveries = []
        for donation in donations:
            if isinstance(donation, GeneralDonation) and donation.need_transportation:
                # Create locations first
                pickup_location = Location.objects.create(
                    latitude=float(fake.latitude()),
                    longitude=float(fake.longitude())
                )
                dropoff_location = Location.objects.create(
                    latitude=float(fake.latitude()),
                    longitude=float(fake.longitude())
                )
                current_location = Location.objects.create(
                    latitude=float(fake.latitude()),
                    longitude=float(fake.longitude())
                )

                # Create delivery with the locations
                delivery = Delivery.objects.create(
                    donation=donation,
                    status=random.choice([s[0] for s in DeliveryStatus.choices]),
                    pickup_location=pickup_location,
                    dropOff_location=dropoff_location,
                    current_location=current_location,
                    pickup_date=fake.date_this_month(),
                    dropOff_date=fake.date_this_month()
                )
                deliveries.append(delivery)
        return deliveries

    def create_volunteers(self, volunteer_users):
        volunteers = []
        for user in volunteer_users:
            volunteer = Volunteer.objects.create(
                user=user,
                skills=json.dumps(random.sample(['Teaching', 'Cooking', 'Cleaning', 'Medical', 'Sports'], k=random.randint(1, 3))),
                availability=json.dumps({
                    'weekdays': random.choice([True, False]),
                    'weekends': random.choice([True, False]),
                    'morning': random.choice([True, False]),
                    'afternoon': random.choice([True, False]),
                    'evening': random.choice([True, False])
                })
            )
            volunteers.append(volunteer)
        return volunteers

    def create_volunteer_offers(self, volunteers):
        offers = []
        for volunteer in volunteers:
            for _ in range(random.randint(1, 3)):
                offer = VolunteerOfferRequest.objects.create(
                    volunteer=volunteer,
                    title=fake.catch_phrase(),
                    description=fake.text(),
                    status=random.choice([s[0] for s in OfferStatus.choices]),
                    is_open=random.choice([True, False])
                )
                offers.append(offer)
        return offers

    def create_need_requests(self, orphanages):
        need_requests = []
        for orphanage in orphanages:
            for _ in range(random.randint(2, 5)):
                request = OrphanageNeedRequest.objects.create(
                    orphanage=orphanage,
                    title=fake.catch_phrase(),
                    description=fake.text(),
                    is_open=True
                )
                need_requests.append(request)
        return need_requests

    def create_matches(self, need_requests, offers):
        matches = []
        for need_request in need_requests:
            if random.random() < 0.7:  # 70% chance of matching
                offer = random.choice(offers)
                match = Matcher.objects.create(
                    need_request=need_request,
                    volunteer_offer=offer
                )
                matches.append(match)
        return matches

    def create_reviews(self, donors, orphanages):
        # Create a pool of donors for each orphanage
        for orphanage in orphanages:
            # Randomly select a subset of donors for this orphanage
            available_donors = random.sample(donors, k=min(5, len(donors)))
            for donor in available_donors:
                Review.objects.create(
                    orphanage=orphanage,
                    donor=donor,
                    stars=random.randint(1, 5),
                    comment=fake.text()
                )

    def create_orphan_sponsorships(self, orphans, donors):
        for orphan in orphans:
            if random.random() < 0.3:  # 30% chance of having a sponsor
                OrphanSponsor.objects.create(
                    orphan=orphan,
                    donor=random.choice(donors),
                    is_active=random.choice([True, False])
                )

    def create_orphan_updates(self, orphans):
        for orphan in orphans:
            for _ in range(random.randint(1, 3)):
                OrphanUpdate.objects.create(
                    orphan=orphan,
                    title=fake.catch_phrase(),
                    note=fake.text()
                )

    def save_user_credentials(self, users_data):
        with open('user_credentials.json', 'w') as f:
            json.dump(users_data, f, indent=2)

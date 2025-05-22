import csv
import math
import pathlib
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import IntegrityError, models
from decimal import Decimal
import random
from faker import Faker

fake = Faker()
Faker.seed(0)

# ── project models ────────────────────────────────────────────────
from accounts.models   import User, Role
from orphanages.models import Orphanage, Orphan, OrphanUpdate, Review
from donations.models  import (
    Donor, Donation, DonationCategory, DonationStatus,
    DonationItem, Campaign, OrphanSponsor
)
from volunteers.models import Volunteer, VolunteerRequest
from logistics.models  import Delivery
from services.route_service import compute_route
from campaigns.models import CampaignCategory


PASSWORD = "pass"          # default password for **all** seeded users


def create_unique_user(role: str, **extra):
    while True:
        try:
            return User.objects.create_user(
                email=fake.unique.email(), password=PASSWORD, role=role, **extra
            )
        except IntegrityError:
            fake.unique.clear()

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    p = math.pi / 180
    dlat = (lat2 - lat1) * p
    dlon = (lon2 - lon1) * p
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def safe_route(pickup, drop):
    """Try real API; fall back to Haversine if 404/429 or key missing."""
    dist, dur, poly = compute_route(pickup, drop)
    if dist:
        return dist, dur, poly
    lat1, lon1 = map(float, pickup.split(","))
    lat2, lon2 = map(float, drop.split(","))
    km = haversine_km(lat1, lon1, lat2, lon2)
    sec = int(km / 40 * 3600)  # assume 40 km/h
    return int(km * 1000), sec, ""

# ───── command ────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = "Seed HopeConnect with demo data + seed_users.csv credentials."

    def add_arguments(self, parser):
        parser.add_argument("--donors",      type=int, default=100)
        parser.add_argument("--orphans",     type=int, default=400)
        parser.add_argument("--orphanages",  type=int, default=12)
        parser.add_argument("--volunteers",  type=int, default=30)

    def handle(self, *args, **opts):
        self.stdout.write(self.style.NOTICE("Seeding data …"))
        today = timezone.now().date()

        # CSV of credentials
        creds_path = pathlib.Path("seed_users.csv")
        with creds_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["email", "role", "password"])

            def new_user(role, **extra):
                u = create_unique_user(role, **extra)
                writer.writerow([u.email, role, PASSWORD])
                return u

            # 1. Orphanages & managers
            orphanages = []
            for _ in range(opts["orphanages"]):
                manager = new_user(Role.ORPHANAGE)
                orphanage = Orphanage.objects.create(
                    name=fake.company(),
                    city=fake.city(),
                    manager=manager,
                    latitude=round(fake.latitude(), 6),
                    longitude=round(fake.longitude(), 6),
                    is_public_approved=fake.boolean(80),
                )
                orphanages.append(orphanage)

            # 2. Orphans
            for _ in range(opts["orphans"]):
                o = Orphan.objects.create(
                    name=fake.name(),
                    orphanage=random.choice(orphanages),
                    gender=random.choice(["M", "F"]),
                    birth_date=fake.date_between("-12y", "-2y"),
                )
                if fake.boolean(40):
                    OrphanUpdate.objects.create(
                        orphan=o,
                        title="Progress update",
                        note=fake.text(120),
                    )

            # 3. Donors
            donors = []
            for _ in range(opts["donors"]):
                user = new_user(Role.DONOR,
                                first_name=fake.first_name(),
                                last_name=fake.last_name())
                donors.append(Donor.objects.create(user=user))

            # 4. Volunteers
            for _ in range(opts["volunteers"]):
                v_user = new_user(Role.VOLUNTEER)
                Volunteer.objects.create(
                    user=v_user,
                    skills=random.sample(
                        ["teaching", "first aid", "sports", "cooking", "coding"], k=2
                    )
                )

            # 5. Emergency campaigns
            campaigns = [
                Campaign.objects.create(
                    title=f"Emergency Relief #{i+1}",
                    category=CampaignCategory.EMERGENCY,
                    goal_amount=Decimal("10000.00"),
                    start=today,
                    is_open=True,
                )
                for i in range(3)
            ]

            # 6. Donations (+deliveries)
            for donor in donors:
                for _ in range(random.randint(1, 5)):
                    cat = random.choice([DonationCategory.MONEY, DonationCategory.PHYSICAL])
                    donation = Donation.objects.create(
                        donor=donor,
                        amount=Decimal(random.randint(10, 200)),
                        currency="usd",
                        category=cat,
                        status=DonationStatus.COMPLETED,
                        campaign=random.choice(campaigns),
                    )
                    if cat == DonationCategory.PHYSICAL:
                        DonationItem.objects.create(
                            donation=donation,
                            description=fake.word(),
                            quantity=random.randint(1, 10),
                            unit="pcs",
                        )
                        pickup = "31.9505,35.1960"
                        drop   = "31.5,35.4"
                        dist, dur, poly = safe_route(pickup, drop)
                        Delivery.objects.create(
                            donation=donation,
                            pickup_latlng=pickup,
                            dropoff_latlng=drop,
                            distance_m=dist,
                            duration_s=dur,
                            polyline=poly,
                            status=random.choice(["pending", "in_transit", "delivered"]),
                        )

            # 7. Sponsorships (unique per donor+orphan)
            all_orphans = list(Orphan.objects.all())
            for donor in donors:
                pool = all_orphans.copy()
                random.shuffle(pool)
                for _ in range(random.randint(0, 3)):
                    if not pool:
                        break
                    orphan = pool.pop()
                    OrphanSponsor.objects.create(
                        donor=donor,
                        orphan=orphan,
                        monthly_amount=Decimal(random.choice([25, 35, 50])),
                        start_date=today.replace(day=1),
                    )

            # 8. Volunteer requests
            for o in orphanages:
                for _ in range(random.randint(1, 3)):
                    VolunteerRequest.objects.create(
                        orphanage=o,
                        need_description=fake.sentence(),
                        required_skills=random.sample(["teaching", "first aid", "sports"], k=1),
                    )

            # 9. Reviews
            for o in orphanages:
                for donor in random.sample(donors, k=min(5, len(donors))):
                    Review.objects.create(
                        orphanage=o,
                        donor=donor.user,
                        stars=random.randint(3, 5),
                        comment=fake.sentence(nb_words=10),
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Demo data generated. Credentials saved to {creds_path.resolve()}"
        ))
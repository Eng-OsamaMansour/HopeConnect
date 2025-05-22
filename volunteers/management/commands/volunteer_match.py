from django.core.management.base import BaseCommand
from volunteers.matcher import match_open_requests
from volunteers.signals import volunteer_assigned

class Command(BaseCommand):
    help = "Match open volunteer requests to available volunteers"

    def handle(self, *args, **opts):
        matches = match_open_requests()
        for req, vol, score in matches:
            volunteer_assigned.send(
                sender=self.__class__,
                request_id=req.id,
                volunteer_id=vol.id,
                score=score,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Assigned {vol} → request {req.id} (score {score:.2f})"))
        if not matches:
            self.stdout.write("No matches found")
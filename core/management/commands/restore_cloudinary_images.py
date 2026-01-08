import cloudinary
import cloudinary.api
from django.core.management.base import BaseCommand
from core.models import HeroSection, About, Skill, TimelineEvent, Project, Service, SocialLink

class Command(BaseCommand):
    help = "Restore Cloudinary images and link them to your database models"

    def handle(self, *args, **options):
        self.stdout.write("Fetching Cloudinary resources...")

        try:
            resources = cloudinary.api.resources(max_results=500)
        except Exception as e:
            self.stderr.write(f"Error fetching Cloudinary resources: {e}")
            return

        self.stdout.write(f"Found {len(resources.get('resources', []))} resources.")

        # Loop through resources
        for res in resources.get('resources', []):
            public_id = res['public_id']
            url = res['secure_url']

            # Example matching logic: match by public_id prefix
            if public_id.startswith("hero_"):
                HeroSection.objects.filter(image__isnull=True).update(image=url)
            elif public_id.startswith("about_"):
                About.objects.filter(image__isnull=True).update(image=url)
            elif public_id.startswith("skill_"):
                Skill.objects.filter(icon__isnull=True).update(icon=url)
            elif public_id.startswith("timeline_"):
                TimelineEvent.objects.filter(icon__isnull=True).update(icon=url)
            elif public_id.startswith("project_"):
                Project.objects.filter(image__isnull=True).update(image=url)
            elif public_id.startswith("service_"):
                Service.objects.filter(icon__isnull=True).update(icon=url)
            elif public_id.startswith("social_"):
                SocialLink.objects.filter(icon__isnull=True).update(icon=url)

        self.stdout.write(self.style.SUCCESS("Cloudinary images restored and linked successfully!"))

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings

class Command(BaseCommand):
    help = 'Setup Django Site for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='noithatvav.vn',
            help='Domain name for the site'
        )
        parser.add_argument(
            '--name',
            type=str,
            default='VAV Furniture',
            help='Site name'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        name = options['name']
        
        try:
            # Try to get existing site with SITE_ID
            site = Site.objects.get(pk=settings.SITE_ID)
            site.domain = domain
            site.name = name
            site.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated existing site: {domain} (ID: {site.id})')
            )
        except Site.DoesNotExist:
            # Create new site
            site = Site.objects.create(
                id=settings.SITE_ID,
                domain=domain,
                name=name
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created new site: {domain} (ID: {site.id})')
            )
        
        # Verify the setup
        self.stdout.write(f'Site configuration:')
        self.stdout.write(f'  ID: {site.id}')
        self.stdout.write(f'  Domain: {site.domain}')
        self.stdout.write(f'  Name: {site.name}')
        self.stdout.write(f'  SITE_ID in settings: {settings.SITE_ID}')
        
        self.stdout.write(
            self.style.SUCCESS('Site setup completed successfully!')
        )

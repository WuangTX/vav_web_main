# Management command to generate sitemap
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils import timezone
from main.models import Product, Project, News
import xml.etree.ElementTree as ET
import os

class Command(BaseCommand):
    help = 'Generate sitemap.xml file with all URLs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='https://noithatvav.vn',
            help='Domain name for the sitemap'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        
        # Create root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 
                  'http://www.sitemaps.org/schemas/sitemap/0.9 '
                  'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

        # Static pages
        static_pages = [
            {'loc': '/', 'priority': '1.0', 'changefreq': 'daily'},
            {'loc': '/about/', 'priority': '0.8', 'changefreq': 'monthly'},
            {'loc': '/products/', 'priority': '0.9', 'changefreq': 'weekly'},
            {'loc': '/projects/', 'priority': '0.9', 'changefreq': 'weekly'},
            {'loc': '/news/', 'priority': '0.8', 'changefreq': 'daily'},
            {'loc': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
            {'loc': '/chatbot/', 'priority': '0.6', 'changefreq': 'monthly'},
        ]

        # Add static pages
        for page in static_pages:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = domain + page['loc']
            ET.SubElement(url, 'lastmod').text = timezone.now().strftime('%Y-%m-%d')
            ET.SubElement(url, 'changefreq').text = page['changefreq']
            ET.SubElement(url, 'priority').text = page['priority']

        # Add products
        try:
            products = Product.objects.all()
            for product in products:
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = f"{domain}/products/{product.slug}/"
                lastmod = product.updated_at if hasattr(product, 'updated_at') else timezone.now()
                ET.SubElement(url, 'lastmod').text = lastmod.strftime('%Y-%m-%d')
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '0.7'
            self.stdout.write(f'Added {products.count()} products to sitemap')
        except Exception as e:
            self.stdout.write(f'Error adding products: {e}')

        # Add projects
        try:
            projects = Project.objects.all()
            for project in projects:
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = f"{domain}/projects/{project.slug}/"
                lastmod = project.updated_at if hasattr(project, 'updated_at') else timezone.now()
                ET.SubElement(url, 'lastmod').text = lastmod.strftime('%Y-%m-%d')
                ET.SubElement(url, 'changefreq').text = 'monthly'
                ET.SubElement(url, 'priority').text = '0.7'
            self.stdout.write(f'Added {projects.count()} projects to sitemap')
        except Exception as e:
            self.stdout.write(f'Error adding projects: {e}')

        # Add news
        try:
            news_items = News.objects.filter(status='published')
            for news in news_items:
                url = ET.SubElement(urlset, 'url')
                ET.SubElement(url, 'loc').text = f"{domain}/news/{news.slug}/"
                lastmod = news.updated_at if hasattr(news, 'updated_at') else news.created_at
                ET.SubElement(url, 'lastmod').text = lastmod.strftime('%Y-%m-%d')
                ET.SubElement(url, 'changefreq').text = 'weekly'
                ET.SubElement(url, 'priority').text = '0.6'
            self.stdout.write(f'Added {news_items.count()} news items to sitemap')
        except Exception as e:
            self.stdout.write(f'Error adding news: {e}')

        # Write to file
        tree = ET.ElementTree(urlset)
        ET.indent(tree, space="  ", level=0)
        
        sitemap_path = os.path.join(settings.BASE_DIR, 'sitemap.xml')
        tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated sitemap at {sitemap_path}')
        )

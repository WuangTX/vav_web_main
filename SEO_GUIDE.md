# SEO Guide for VAV Furniture Website

## 📋 Files Created

### 1. robots.txt
- **Location**: Root directory
- **Purpose**: Tells search engines which pages to crawl
- **Features**:
  - Allows all content by default
  - Blocks admin and private areas
  - Includes sitemap location
  - Controls bot crawl rates

### 2. sitemap.xml
- **Location**: Root directory  
- **Purpose**: Lists all important URLs for search engines
- **Features**:
  - Static pages (home, about, contact, etc.)
  - Dynamic product URLs
  - Dynamic project URLs
  - Dynamic news URLs
  - Proper priority and update frequency

### 3. sitemaps.py
- **Location**: Root directory
- **Purpose**: Django sitemap framework for dynamic generation
- **Features**:
  - Automatic sitemap generation
  - Real-time updates when content changes
  - Proper lastmod dates from database

### 4. Enhanced base.html
- **Location**: templates/base.html
- **Purpose**: SEO meta tags for all pages
- **Features**:
  - Title and description tags
  - Open Graph (Facebook) tags
  - Twitter Card tags
  - Structured data (JSON-LD)
  - Canonical URLs
  - Proper favicon setup

## 🚀 Setup Instructions

### 1. Update Domain Names
Domain has been updated to `https://noithatvav.vn` in:
- ✅ `robots.txt`
- ✅ `sitemap.xml`
- ✅ `sitemaps.py`
- ✅ `setup_seo.bat`
- ✅ `generate_sitemap.py`

### 2. Run SEO Setup
```bash
# Run the setup script
setup_seo.bat

# Or manually run:
python manage.py generate_sitemap --domain=https://noithatvav.vn
python manage.py collectstatic
```

### 3. Django Settings
Add to your `settings.py`:
```python
# Add 'django.contrib.sitemaps' to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing apps
    'django.contrib.sitemaps',
    'django.contrib.sites',
]

SITE_ID = 1
```

### 4. URL Configuration
The URLs are already configured in `vav_furniture/urls.py`:
- `/robots.txt` - Serves robots.txt file
- `/sitemap.xml` - Serves dynamic sitemap

## 📊 SEO Features Implemented

### Meta Tags
- ✅ Title tags (unique per page)
- ✅ Meta descriptions
- ✅ Meta keywords
- ✅ Robots meta tags
- ✅ Canonical URLs

### Social Media
- ✅ Open Graph tags (Facebook)
- ✅ Twitter Card tags
- ✅ Social media images

### Structured Data
- ✅ Organization schema
- ✅ Contact information
- ✅ Business details

### Technical SEO
- ✅ robots.txt
- ✅ XML sitemap
- ✅ Proper HTML structure
- ✅ Mobile-friendly viewport
- ✅ Fast loading CSS/JS

## 🔧 Customization

### Add New Pages to Sitemap
Edit `sitemaps.py` and add to `StaticViewSitemap`:
```python
def items(self):
    return ['main:home', 'main:about', 'main:new_page']
```

### Custom Meta Tags per Page
In your templates, use blocks:
```html
{% block title %}Custom Page Title{% endblock %}
{% block description %}Custom page description{% endblock %}
{% block keywords %}custom, keywords, here{% endblock %}
```

### Product/Project SEO
Ensure your models have:
- `slug` field for URLs
- `updated_at` timestamp
- SEO-friendly titles
- Meta descriptions

## 📈 Next Steps

### 1. Submit to Search Engines
- **Google Search Console**: https://search.google.com/search-console
- **Bing Webmaster Tools**: https://www.bing.com/webmasters

### 2. Verify Setup
- Check robots.txt: `noithatvav.vn/robots.txt`
- Check sitemap: `noithatvav.vn/sitemap.xml`
- Test structured data: https://search.google.com/test/rich-results

### 3. Monitor Performance
- Set up Google Analytics
- Monitor search rankings
- Track crawl errors
- Review sitemap submission status

### 4. Content Optimization
- Write unique meta descriptions
- Optimize image alt tags
- Use heading tags properly (H1, H2, H3)
- Internal linking strategy
- Regular content updates

## 🛠️ Maintenance

### Auto-generate Sitemap
Set up a cron job to regenerate sitemap:
```bash
# Every day at 3 AM
0 3 * * * cd /path/to/project && python manage.py generate_sitemap
```

### Monitor SEO Health
- Check for 404 errors
- Monitor page load speeds
- Verify mobile-friendliness
- Track search rankings
- Update sitemaps when adding new content

## 📞 Support

If you need help with SEO implementation:
1. Check Django documentation for sitemaps
2. Use Google Search Console for errors
3. Test with SEO tools like Screaming Frog
4. Monitor Google Analytics for traffic

---

**Note**: Remember to update all domain references and customize content according to your specific business needs.

# Google Search Console Sitemap Submission Guide
# For noithatvav.vn

## 🎯 Cách Submit Sitemap cho noithatvav.vn

### 1. Google Search Console
- Truy cập: https://search.google.com/search-console
- Thêm property: noithatvav.vn
- Verify ownership (HTML tag hoặc DNS)
- Vào Sitemaps → Add new sitemap
- Nhập: sitemap.xml
- Click Submit

### 2. Bing Webmaster Tools  
- Truy cập: https://www.bing.com/webmasters
- Add site: noithatvav.vn
- Verify ownership
- Submit sitemap: https://noithatvav.vn/sitemap.xml

### 3. URLs cần kiểm tra sau khi deploy:
- ✅ https://noithatvav.vn/robots.txt
- ✅ https://noithatvav.vn/sitemap.xml
- ✅ https://noithatvav.vn/admin/ (should be blocked)

### 4. Meta tags đã tối ưu cho noithatvav.vn:
```html
<title>Nội Thất Cao Cấp VAV - noithatvav.vn</title>
<meta name="description" content="VAV Furniture - Chuyên cung cấp nội thất cao cấp, thiết kế đẹp tại noithatvav.vn">
<meta property="og:url" content="https://noithatvav.vn">
<link rel="canonical" href="https://noithatvav.vn">
```

### 5. Structured Data cho Business:
```json
{
  "@context": "https://schema.org",
  "@type": "Organization", 
  "name": "VAV Furniture",
  "url": "https://noithatvav.vn",
  "logo": "https://noithatvav.vn/static/images/logo.png"
}
```

### 6. Priority Pages trong Sitemap:
- Homepage (/) - Priority: 1.0
- Products (/products/) - Priority: 0.9  
- Projects (/projects/) - Priority: 0.9
- About (/about/) - Priority: 0.8
- News (/news/) - Priority: 0.8
- Contact (/contact/) - Priority: 0.7
- Chatbot (/chatbot/) - Priority: 0.6

### 7. Analytics Setup:
```html
<!-- Google Analytics for noithatvav.vn -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 8. Performance Checks:
- PageSpeed Insights: https://pagespeed.web.dev/
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
- Rich Results Test: https://search.google.com/test/rich-results

### 9. Local SEO cho Vietnam:
```html
<meta property="og:locale" content="vi_VN">
<html lang="vi">
<meta name="geo.region" content="VN">
<meta name="geo.placename" content="Vietnam">
```

### 10. Social Media Integration:
- Facebook: https://www.facebook.com/vav.furniture
- Instagram: https://www.instagram.com/vav.furniture  
- YouTube: https://www.youtube.com/c/vavfurniture

## 📊 KPIs to Monitor:
- Organic search traffic
- Keyword rankings  
- Page load speed
- Mobile usability
- Core Web Vitals
- Crawl errors
- Sitemap submission status

## 🚀 Next Steps after Deploy:
1. Run: `python manage.py generate_sitemap --domain=https://noithatvav.vn`
2. Submit sitemap to Google Search Console
3. Submit sitemap to Bing Webmaster Tools
4. Set up Google Analytics
5. Configure Facebook Pixel (if needed)
6. Monitor search rankings
7. Set up Google My Business (if physical location)

## ⚡ Quick Commands:
```bash
# Generate fresh sitemap
python manage.py generate_sitemap --domain=https://noithatvav.vn

# Check robots.txt
curl https://noithatvav.vn/robots.txt

# Check sitemap
curl https://noithatvav.vn/sitemap.xml

# Validate HTML
validator.w3.org/nu/?doc=https://noithatvav.vn
```

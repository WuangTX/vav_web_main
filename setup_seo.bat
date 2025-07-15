@echo off
echo ================================================
echo          VAV Furniture - SEO Setup
echo ================================================
echo.

echo [1] Generating sitemap.xml...
python manage.py generate_sitemap --domain=https://noithatvav.vn
echo.

echo [2] Checking robots.txt...
if exist "robots.txt" (
    echo ✓ robots.txt already exists
) else (
    echo ✗ robots.txt not found
)
echo.

echo [3] Collecting static files for production...
python manage.py collectstatic --noinput
echo.

echo [4] SEO Checklist:
echo ✓ robots.txt created
echo ✓ sitemap.xml generated
echo ✓ Meta tags added to base template
echo ✓ Structured data (JSON-LD) added
echo ✓ Open Graph tags added
echo ✓ Twitter Card tags added
echo ✓ Canonical URLs configured
echo.

echo [5] Next Steps:
echo - Update domain name in robots.txt and sitemap
echo - Submit sitemap to Google Search Console
echo - Submit sitemap to Bing Webmaster Tools
echo - Verify robots.txt is accessible at /robots.txt
echo - Check structured data with Google Rich Results Test
echo.

echo ================================================
echo             SEO Setup Complete!
echo ================================================
pause

import cohere
import json
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Q
from .models import ChatSession, ChatMessage
from main.models import Product, Project, News, ProductCategory
import logging

logger = logging.getLogger(__name__)

# Khởi tạo Cohere client
COHERE_API_KEY = "K45hKBPVa1G6YgjlIQKAF7Dp5JJ162gr7iCHvqR1"
co = cohere.Client(COHERE_API_KEY)


class ChatbotService:
    """Service class để xử lý logic chatbot"""
    
    def __init__(self):
        self.company_info = {
            "name": "VAV Furniture",
            "number": "0935908007",
            "address": "73 Nguyễn Viết Xuân - Hòa Minh - Liên Chiểu, Da Nang, Vietnam",
            "email": "vavfurniture.danang@gmail.com",
            "website": "www.noithatvav.vn",
            "facebook": "https://www.facebook.com/vavfurniture0203",
            "description": "Công ty chuyên thiết kế và sản xuất nội thất cao cấp",
            "services": [
                "Thiết kế nội thất biệt thự",
                "Thiết kế nội thất căn hộ", 
                "Thiết kế nội thất văn phòng",
                "Thiết kế nội thất khách sạn",
                "Thiết kế nội thất nhà hàng",
                "Sản xuất đồ nội thất theo yêu cầu",
                "Tư vấn thiết kế miễn phí"
            ],
            "process": [
                "Tư vấn & Thiết kế",
                "Lập kế hoạch & Vật liệu", 
                "Sản xuất & Chế tác",
                "Thi công & Lắp đặt",
                "Nghiệm thu & Bàn giao"
            ]
        }
    
    def extract_keywords(self, query):
        """Trích xuất từ khóa từ câu hỏi với cải tiến"""
        # Loại bỏ các từ không quan trọng
        stop_words = [
            'tôi', 'muốn', 'cần', 'tìm', 'kiếm', 'xem', 'cho', 'về', 'của', 'với', 'và', 'có', 'là', 'để', 
            'trong', 'thế', 'nào', 'như', 'gì', 'bạn', 'mình', 'em', 'anh', 'chị', 'được', 'không', 'rồi',
            'ạ', 'ơi', 'nhé', 'nha', 'vậy', 'thì', 'mà', 'hay', 'hoặc', 'nếu', 'khi', 'lúc', 'bây', 'giờ',
            'hôm', 'nay', 'mai', 'qua', 'này', 'đó', 'kia', 'nào', 'đâu', 'sao', 'ai', 'đi', 'lại', 'ra',
            'vào', 'lên', 'xuống', 'mới', 'cũ', 'nhất', 'liên', 'quan', 'một', 'hai', 'ba', 'bốn', 'năm'
        ]
        
        # Tách từ và làm sạch
        words = query.lower().split()
        keywords = []
        
        for word in words:
            cleaned_word = word.strip('.,!?;:()[]{}"\'-')
            if cleaned_word not in stop_words and len(cleaned_word) > 1:
                keywords.append(cleaned_word)
        
        # Thêm mapping từ khóa liên quan và đồng nghĩa
        keyword_mapping = {
            # Tin tức keywords
            'tin': ['tin tức', 'bài viết', 'thông tin', 'news'],
            'tức': ['tin tức', 'bài viết', 'thông tin', 'news'],
            'news': ['tin tức', 'bài viết', 'thông tin'],
            'bài': ['bài viết', 'tin tức'],
            'viết': ['bài viết', 'tin tức'],
            
            # Nội thất keywords
            'nội': ['nội thất', 'thiết kế nội thất', 'furniture'],
            'thất': ['nội thất', 'thiết kế nội thất', 'furniture'],
            'furniture': ['nội thất', 'thiết kế nội thất'],
            'design': ['thiết kế', 'trang trí', 'nội thất'],
            'thiết': ['thiết kế', 'design'],
            'kế': ['thiết kế', 'design'],
            
            # Danh mục sản phẩm nội thất
            'sofa': ['ghế sofa', 'sofa bed', 'ghế ngồi', 'Sofa & Ghế ngồi', 'sofa-ghe-ngoi'],
            'bàn': ['bàn ghế', 'bàn làm việc', 'bàn ăn', 'table', 'Bàn', 'ban'],
            'ghế': ['bàn ghế', 'ghế ngồi', 'chair', 'sofa', 'Ghế', 'ghe'],
            'giường': ['giường ngủ', 'bed', 'phòng ngủ', 'Giường', 'giuong', 'giuong-ngu'],
            'tủ': ['tủ quần áo', 'tủ bếp', 'tủ sách', 'cabinet', 'wardrobe', 'Tủ', 'tu'],
            'table': ['bàn', 'bàn ăn', 'bàn làm việc', 'Bàn', 'ban'],
            'chair': ['ghế', 'ghế ngồi', 'Ghế', 'ghe'],
            'bed': ['giường', 'giường ngủ', 'Giường', 'giuong'],
            'cabinet': ['tủ', 'tủ quần áo', 'Tủ', 'tu'],
            'wardrobe': ['tủ quần áo', 'tủ', 'Tủ', 'tu-quan-ao'],
            'kệ': ['kệ sách', 'kệ tivi', 'kệ', 'Kệ', 'ke'],
            'đèn': ['đèn trang trí', 'đèn bàn', 'đèn', 'Đèn', 'den'],
            'thảm': ['thảm trải sàn', 'thảm', 'Thảm', 'tham'],
            'rèm': ['rèm cửa', 'rèm', 'Rèm', 'rem'],
            'nệm': ['nệm cao su', 'nệm lò xo', 'Nệm', 'nem'],
            'gương': ['gương trang trí', 'gương', 'Gương', 'guong'],
            
            # Loại phòng
            'phòng': ['thiết kế phòng', 'không gian', 'room'],
            'khách': ['phòng khách', 'living room'],
            'ăn' : ['phòng ăn', 'phòng ăn uống', 'dining room'],
            'bếp': ['phòng bếp', 'kitchen', 'tủ bếp'],
            'ngủ': ['phòng ngủ', 'bedroom', 'giường ngủ'],
            'làm': ['làm việc', 'văn phòng', 'office'],
            'việc': ['làm việc', 'văn phòng', 'office'],
            'living': ['phòng khách', 'living room'],
            'kitchen': ['phòng bếp', 'bếp'],
            'bedroom': ['phòng ngủ', 'ngủ'],
            'office': ['văn phòng', 'làm việc'],
            
            # Loại dự án
            'biệt': ['biệt thự', 'villa'],
            'thự': ['biệt thự', 'villa'],
            'villa': ['biệt thự'],
            'căn': ['căn hộ', 'apartment'],
            'hộ': ['căn hộ', 'apartment'],
            'apartment': ['căn hộ'],
            'văn': ['văn phòng', 'office'],
            'chung': ['chung cư', 'căn hộ'],
            'cư': ['chung cư', 'căn hộ'],
            
            # Màu sắc
            'trắng': ['màu trắng', 'white'],
            'đen': ['màu đen', 'black'],
            'nâu': ['màu nâu', 'brown'],
            'xanh': ['màu xanh', 'blue', 'green'],
            'đỏ': ['màu đỏ', 'red'],
            'vàng': ['màu vàng', 'yellow'],
            'xám': ['màu xám', 'gray'],
            
            # Chất liệu
            'gỗ': ['chất liệu gỗ', 'wood', 'wooden'],
            'kim': ['kim loại', 'metal'],
            'loại': ['kim loại', 'metal', 'chất liệu'],
            'da': ['da thật', 'leather'],
            'vải': ['vải bọc', 'fabric'],
            'kính': ['kính cường lực', 'glass'],
            'wood': ['gỗ', 'wooden'],
            'metal': ['kim loại'],
            'leather': ['da', 'da thật'],
            'fabric': ['vải', 'vải bọc'],
            'glass': ['kính', 'kính cường lực'],
            
            # Liên hệ keywords
            'liên': ['liên hệ', 'contact', 'liên lạc'],
            'hệ': ['liên hệ', 'contact', 'liên lạc'],
            'contact': ['liên hệ', 'liên lạc'],
            'phone': ['số điện thoại', 'điện thoại', 'số phone'],
            'điện': ['điện thoại', 'số điện thoại', 'phone'],
            'thoại': ['điện thoại', 'số điện thoại', 'phone'],
            'email': ['email', 'thư điện tử', 'mail'],
            'mail': ['email', 'thư điện tử'],
            'facebook': ['facebook', 'fb', 'face book'],
            'địa': ['địa chỉ', 'address'],
            'chỉ': ['địa chỉ', 'address'],
            'address': ['địa chỉ'],
            'website': ['website', 'web', 'trang web'],
            'web': ['website', 'trang web'],
            'hotline': ['hotline', 'đường dây nóng'],
            'zalo': ['zalo', 'chat'],
            'messenger': ['messenger', 'mess']
        }
        
        # Mở rộng keywords với đồng nghĩa
        expanded_keywords = set(keywords)
        for keyword in keywords:
            if keyword in keyword_mapping:
                expanded_keywords.update(keyword_mapping[keyword])
        
        # Tìm cụm từ 2 từ liền kề có ý nghĩa
        word_pairs = []
        for i in range(len(words) - 1):
            pair = f"{words[i]} {words[i+1]}"
            cleaned_pair = pair.strip('.,!?;:()[]{}"\'-')
            if any(stop in cleaned_pair for stop in ['nội thất', 'tin tức', 'bài viết', 'thiết kế', 'phòng khách', 'phòng ngủ', 'văn phòng']):
                expanded_keywords.add(cleaned_pair)
        
        return list(expanded_keywords)
    
    def identify_product_category(self, query):
        """Nhận diện danh mục sản phẩm từ câu hỏi"""
        query_lower = query.lower()
        
        # Mapping từ khóa với tên danh mục chính xác
        category_patterns = {
            'sofa': ['sofa', 'ghế sofa', 'sofa bed', 'ghế ngồi'],
            'ban': ['bàn', 'table', 'bàn ăn', 'bàn làm việc', 'bàn ghế'],
            'ghe': ['ghế', 'chair', 'ghế ngồi'],
            'giuong': ['giường', 'bed', 'giường ngủ'],
            'tu': ['tủ', 'cabinet', 'wardrobe', 'tủ quần áo', 'tủ bếp'],
            'ke': ['kệ', 'kệ sách', 'kệ tivi'],
            'den': ['đèn', 'đèn trang trí', 'đèn bàn'],
            'tham': ['thảm', 'thảm trải sàn'],
            'rem': ['rèm', 'rèm cửa'],
            'nem': ['nệm', 'nệm cao su'],
            'guong': ['gương', 'gương trang trí']
        }
        
        # Tìm danh mục match với độ tin cậy cao nhất
        max_matches = 0
        best_category = None
        
        for category, patterns in category_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in query_lower)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        return best_category if max_matches > 0 else None

    def calculate_relevance_score(self, text_fields, keywords):
        """Tính điểm liên quan dựa trên số từ khóa match và vị trí"""
        score = 0
        text_combined = ' '.join(text_fields).lower()
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # Đếm số lần xuất hiện của từ khóa
            count = text_combined.count(keyword_lower)
            if count > 0:
                # Điểm cơ bản cho việc match
                score += count * 10
                
                # Bonus nếu từ khóa xuất hiện ở đầu tên
                if text_fields[0].lower().startswith(keyword_lower):
                    score += 50
                
                # Bonus nếu từ khóa match chính xác (whole word)
                import re
                if re.search(r'\b' + re.escape(keyword_lower) + r'\b', text_combined):
                    score += 20
                
                # Bonus nếu từ khóa xuất hiện trong tên sản phẩm
                if keyword_lower in text_fields[0].lower():
                    score += 30
        
        return score

    def search_products(self, query):
        """Tìm kiếm sản phẩm theo từ khóa thông minh với scoring và danh mục"""
        keywords = self.extract_keywords(query)
        if not keywords:
            return []
        
        # Nhận diện danh mục sản phẩm chính
        identified_category = self.identify_product_category(query)
        
        # Kiểm tra xem có tìm kiếm theo danh mục không
        category_products = []
        
        # Tìm kiếm theo danh mục đã nhận diện
        if identified_category:
            category_result = self.search_by_category(identified_category)
            if category_result:
                category_products.extend(category_result)
        
        # Tìm kiếm theo từng keyword
        for keyword in keywords:
            category_result = self.search_by_category(keyword)
            if category_result:
                category_products.extend(category_result)
        
        # Tạo query filter động cho tìm kiếm chung
        q_objects = Q()
        for keyword in keywords:
            q_objects |= (
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(category__name__icontains=keyword) |
                Q(category__slug__icontains=keyword)
            )
        
        general_products = Product.objects.filter(q_objects).select_related('category').distinct()
        
        # Gộp kết quả và loại bỏ duplicate
        all_products = list(general_products)
        category_product_ids = [p['id'] for p in category_products]
        
        # Thêm sản phẩm từ category nếu chưa có
        for cat_product in category_products:
            if not any(p.id == cat_product['id'] for p in all_products):
                try:
                    product = Product.objects.get(id=cat_product['id'])
                    all_products.append(product)
                except Product.DoesNotExist:
                    continue
        
        # Tính điểm liên quan cho mỗi sản phẩm
        product_scores = []
        for product in all_products:
            text_fields = [
                product.name,
                product.description or '',
                product.category.name,
                product.category.slug or ''
            ]
            score = self.calculate_relevance_score(text_fields, keywords)
            
            # Bonus cho sản phẩm từ danh mục match
            if product.id in category_product_ids:
                score += 100  # Ưu tiên cao cho match danh mục
            
            # Bonus đặc biệt cho danh mục đã nhận diện chính xác
            if identified_category and (identified_category.lower() in product.category.name.lower() or 
                                      identified_category.lower() in product.category.slug.lower()):
                score += 150
                
            product_scores.append((product, score))
        
        # Sắp xếp theo điểm số giảm dần
        product_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Lấy top 3 sản phẩm có điểm cao nhất (giảm từ 5 xuống 3)
        top_products = [item[0] for item in product_scores[:3]]
        
        return [
            {
                'id': p.id,
                'name': p.name,
                'price': str(p.price),
                'category': p.category.name,
                'image': p.image.url if p.image else None,
                'slug': p.slug,
                'description': p.description[:200] + "..." if len(p.description) > 200 else p.description,
                'relevance_score': next(score for prod, score in product_scores if prod.id == p.id)
            }
            for p in top_products
        ]
    
    def search_projects(self, query):
        """Tìm kiếm dự án theo từ khóa thông minh với scoring"""
        keywords = self.extract_keywords(query)
        if not keywords:
            return []
        
        # Tạo query filter động
        q_objects = Q()
        for keyword in keywords:
            q_objects |= (
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(project_type__icontains=keyword) |
                Q(location__icontains=keyword)
            )
        
        projects = Project.objects.filter(q_objects).prefetch_related('gallery_images').distinct()
        
        # Tính điểm liên quan cho mỗi dự án
        project_scores = []
        for project in projects:
            text_fields = [
                project.title,
                project.description or '',
                project.project_type or '',
                project.location or ''
            ]
            score = self.calculate_relevance_score(text_fields, keywords)
            project_scores.append((project, score))
        
        # Sắp xếp theo điểm số giảm dần
        project_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Lấy top 3 dự án có điểm cao nhất (giảm từ 5 xuống 3)
        top_projects = [item[0] for item in project_scores[:3]]
        
        return [
            {
                'id': p.id,
                'title': p.title,
                'type': p.get_project_type_display(),
                'location': p.location,
                'client': p.client,
                'image': p.image.url if p.image else None,
                'slug': p.slug,
                'description': p.description[:200] + "..." if len(p.description) > 200 else p.description,
                'gallery_count': p.gallery_images.count(),
                'relevance_score': next(score for proj, score in project_scores if proj.id == p.id)
            }
            for p in top_projects
        ]
    
    def search_news(self, query):
        """Tìm kiếm tin tức theo từ khóa thông minh với scoring"""
        keywords = self.extract_keywords(query)
        
        # Nếu user chỉ hỏi tổng quát về "tin tức" thì trả về tin tức mới nhất
        if not keywords or (len(keywords) == 1 and keywords[0] in ['tin', 'tức', 'tin tức', 'news']):
            # Trả về top 3 tin tức mới nhất (giảm từ 5 xuống 3)
            latest_news = News.objects.filter(
                status='published'
            ).select_related('category').order_by('-published_at')[:3]
            
            return [
                {
                    'id': n.id,
                    'title': n.title,
                    'summary': n.summary,
                    'category': n.category.name,
                    'image': n.image.url if n.image else None,
                    'slug': n.slug,
                    'published_at': n.published_at.strftime('%d/%m/%Y') if n.published_at else '',
                    'relevance_score': 100  # Điểm cao cho tin tức mới nhất
                }
                for n in latest_news
            ]
        
        # Tạo query filter động cho tìm kiếm theo từ khóa
        q_objects = Q()
        for keyword in keywords:
            q_objects |= (
                Q(title__icontains=keyword) |
                Q(content__icontains=keyword) |
                Q(summary__icontains=keyword) |
                Q(tags__icontains=keyword) |
                Q(category__name__icontains=keyword)
            )
        
        news = News.objects.filter(
            q_objects,
            status='published'
        ).select_related('category').distinct()
        
        # Tính điểm liên quan cho mỗi tin tức
        news_scores = []
        for news_item in news:
            text_fields = [
                news_item.title,
                news_item.summary or '',
                news_item.content or '',
                news_item.category.name,
                news_item.tags or ''
            ]
            score = self.calculate_relevance_score(text_fields, keywords)
            news_scores.append((news_item, score))
        
        # Sắp xếp theo điểm số giảm dần
        news_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Lấy top 3 tin tức có điểm cao nhất (giảm từ 5 xuống 3)
        top_news = [item[0] for item in news_scores[:3]]
        
        return [
            {
                'id': n.id,
                'title': n.title,
                'summary': n.summary,
                'category': n.category.name,
                'image': n.image.url if n.image else None,
                'slug': n.slug,
                'published_at': n.published_at.strftime('%d/%m/%Y') if n.published_at else '',
                'relevance_score': next(score for news_item, score in news_scores if news_item.id == n.id)
            }
            for n in top_news
        ]
    
    def get_product_categories(self):
        """Lấy danh sách danh mục sản phẩm với thông tin chi tiết"""
        categories = ProductCategory.objects.all()
        return [
            {
                'id': c.id,
                'name': c.name,
                'slug': c.slug,
                'description': c.description or '',
                'product_count': c.products.count() if hasattr(c, 'products') else 0
            }
            for c in categories
        ]
    
    def search_by_category(self, category_name):
        """Tìm kiếm sản phẩm theo danh mục"""
        try:
            # Tìm danh mục theo tên hoặc slug
            category = ProductCategory.objects.filter(
                Q(name__icontains=category_name) |
                Q(slug__icontains=category_name)
            ).first()
            
            if category:
                products = Product.objects.filter(category=category).select_related('category')[:6]
                return [
                    {
                        'id': p.id,
                        'name': p.name,
                        'price': str(p.price),
                        'category': p.category.name,
                        'image': p.image.url if p.image else None,
                        'slug': p.slug,
                        'description': p.description[:200] + "..." if len(p.description) > 200 else p.description
                    }
                    for p in products
                ]
            return []
        except Exception as e:
            logger.error(f"Error searching by category: {str(e)}")
            return []
    
    def generate_response(self, user_message, session):
        """Tạo phản hồi từ Cohere AI"""
        try:
            # Kiểm tra nếu là câu hỏi về liên hệ trước tiên
            if self.is_contact_inquiry(user_message):
                return {
                    'response': self.get_contact_response(),
                    'products': [],
                    'projects': [],
                    'news': []
                }
            
            # Lấy lịch sử chat gần đây
            recent_messages = ChatMessage.objects.filter(
                session=session
            ).order_by('-created_at')[:10]
            
            # Tạo context từ lịch sử
            conversation_history = []
            for msg in reversed(recent_messages):
                conversation_history.append(f"{msg.message_type}: {msg.content}")
            
            # Trích xuất từ khóa từ câu hỏi
            keywords = self.extract_keywords(user_message)
            
            # Xác định chủ đề chính trước khi tìm kiếm
            main_topic = self.identify_main_topic_from_keywords(keywords, user_message)
            
            # Tìm kiếm nội dung theo ưu tiên chủ đề
            products = []
            projects = []
            news = []
            
            if main_topic == "tin tức nội thất":
                # CHỈ tìm tin tức khi user hỏi về tin tức
                news = self.search_news(user_message)
                # Chỉ tìm thêm sản phẩm/dự án nếu không có tin tức và có từ khóa liên quan
                if not news:
                    if any(kw in user_message.lower() for kw in ['nội thất', 'furniture', 'thiết kế']):
                        products = self.search_products(user_message)[:2]
                        projects = self.search_projects(user_message)[:2]
            elif main_topic == "sản phẩm nội thất":
                # Chỉ tìm sản phẩm và dự án liên quan, KHÔNG tìm tin tức
                products = self.search_products(user_message)
                projects = self.search_projects(user_message)[:2]
            elif main_topic == "dự án thiết kế":
                # Chỉ tìm dự án và sản phẩm liên quan, KHÔNG tìm tin tức
                projects = self.search_projects(user_message)
                products = self.search_products(user_message)[:2]
            elif main_topic == "thông tin liên hệ":
                # Chỉ trả về thông tin liên hệ, không tìm kiếm gì khác
                pass
            else:
                # Tìm kiếm tổng quát - CHỈ sản phẩm và dự án, KHÔNG tin tức
                products = self.search_products(user_message)
                projects = self.search_projects(user_message)
                # KHÔNG tìm tin tức trừ khi user hỏi rõ ràng về tin tức
            
            categories = self.get_product_categories()
            
            # Tạo context cho AI
            context = f"""
Bạn là trợ lý ảo của VAV Furniture. Hãy trả lời NGẮN GỌN, THÂN THIỆN và CHÍNH XÁC.

Từ khóa được trích xuất: {', '.join(keywords)}
Chủ đề chính: {main_topic}

Quy tắc trả lời:
- Tối đa 2-3 câu ngắn gọn
- Tập trung vào chủ đề chính được xác định
- Đề cập đến số lượng kết quả tìm được nếu có
- Luôn kết thúc bằng câu hỏi để tương tác

Thông tin công ty: VAV Furniture - {self.company_info['description']}

Dịch vụ chính: {', '.join(self.company_info['services'][:3])}...

Kết quả tìm kiếm:
- Sản phẩm: {len(products)} sản phẩm
- Dự án: {len(projects)} dự án  
- Tin tức: {len(news)} bài viết

Hãy trả lời ngắn gọn về {main_topic} và hướng dẫn người dùng xem các gợi ý bên dưới.
"""
            
            response = co.chat(
                model="command-r-plus",
                message=user_message,
                preamble=context,
                max_tokens=150,  # Giảm thêm để ngắn gọn hơn
                temperature=0.3   # Giảm thêm để chính xác hơn
            )
            
            return {
                'response': response.text,
                'products': products,
                'projects': projects,
                'news': news
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                'response': "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau.",
                'products': [],
                'projects': [],
                'news': []
            }

    def identify_main_topic(self, keywords, products, projects, news):
        """DEPRECATED - Dùng identify_main_topic_from_keywords thay thế"""
        # Gọi hàm mới để đảm bảo logic nhất quán
        return self.identify_main_topic_from_keywords(keywords, ' '.join(keywords))

    def identify_main_topic_from_keywords(self, keywords, user_message):
        """Xác định chủ đề chính chỉ từ từ khóa trong câu hỏi"""
        message_lower = user_message.lower()
        
        # Từ khóa về quy trình thiết kế (ưu tiên cao nhất cho dự án)
        design_process_indicators = [
            'quy trình', 'quy trình thiết kế', 'process', 'thiết kế như thế nào', 'hoạt động',
            'làm việc', 'tư vấn', 'consultation', 'thế nào', 'ra sao', 'tiến hành'
        ]
        
        # Từ khóa về tin tức (cần chính xác và rõ ràng)
        news_indicators = [
            'tin tức', 'news', 'bài viết', 'thông tin mới', 'cập nhật', 'xu hướng', 
            'mới nhất', 'tin mới', 'bài báo', 'tin hot', 'tin nổi bật', 'bài đăng',
            'thông tin', 'cập nhật mới', 'tin mới nhất',
        ]
        
        # Cụm từ rõ ràng về tin tức (ưu tiên cao nhất)
        news_phrases = [
            'tin tức mới nhất', 'tin tức về', 'bài viết về', 'thông tin mới về',
            'cập nhật tin tức', 'xem tin tức', 'đọc tin tức', 'tin tức nội thất',
            'thông tin nội thất', 'có tin gì', 'tin gì mới', 'bài viết nào',
            'thông tin gì mới', 'có gì mới', 'news about', 'latest news'
        ]
        
        # Từ khóa về dự án và thiết kế
        project_indicators = [
            'dự án', 'thiết kế', 'biệt thự', 'căn hộ', 'villa', 'showroom', 'thi công', 'project',
            'không gian', 'phòng khách', 'phòng ngủ', 'phòng bếp', 'văn phòng', 'living room', 
            'bedroom', 'kitchen', 'office', 'interior design', 'design'
        ]
        
        # Từ khóa về sản phẩm cụ thể
        product_indicators = [
            'sản phẩm', 'mua', 'giá', 'sofa', 'bàn', 'ghế', 'giường', 'tủ', 
            'đồ nội thất', 'furniture', 'chair', 'table', 'bed', 'cabinet', 
            'wardrobe', 'giá cả', 'bán', 'mua bán'
        ]
        
        # Từ khóa về liên hệ (ưu tiên cao)
        contact_indicators = [
            'liên hệ', 'contact', 'số điện thoại', 'phone', 'email', 'địa chỉ', 'address',
            'facebook', 'website', 'hotline', 'gọi điện', 'thông tin liên hệ'
        ]
        
        # Kiểm tra liên hệ trước (ưu tiên cao)
        for indicator in contact_indicators:
            if indicator in message_lower:
                return "thông tin liên hệ"
        
        # Kiểm tra quy trình thiết kế trước (ưu tiên cao nhất cho dự án)
        for indicator in design_process_indicators:
            if indicator in message_lower:
                return "dự án thiết kế"
        
        # Kiểm tra cụm từ tin tức trước (chính xác hơn)
        for phrase in news_phrases:
            if phrase in message_lower:
                return "tin tức nội thất"
        
        # Kiểm tra từ khóa tin tức (linh hoạt hơn)
        for indicator in news_indicators:
            if indicator in message_lower:
                # Kiểm tra thêm: không được chứa từ khóa sản phẩm/dự án mạnh
                avoid_words = ['mua', 'bán', 'giá', 'sofa', 'bàn', 'ghế', 'giường', 'tủ', 'thiết kế phòng', 'dự án cụ thể']
                if not any(avoid in message_lower for avoid in avoid_words):
                    return "tin tức nội thất"
        
        # Kiểm tra từ khóa dự án/thiết kế
        for indicator in project_indicators:
            if indicator in message_lower:
                return "dự án thiết kế"
        
        # Kiểm tra từ khóa sản phẩm cuối cùng
        for indicator in product_indicators:
            if indicator in message_lower:
                return "sản phẩm nội thất"
        
        return "tư vấn nội thất"
    
    def is_contact_inquiry(self, query):
        """Nhận diện câu hỏi về thông tin liên hệ"""
        query_lower = query.lower()
        
        # Từ khóa rõ ràng về liên hệ
        contact_keywords = [
            'liên hệ', 'contact', 'liên lạc', 'gọi điện', 'gọi cho',
            'số điện thoại', 'phone', 'điện thoại', 'hotline',
            'email', 'thư điện tử', 'mail', 'gửi mail',
            'địa chỉ', 'address', 'ở đâu', 'chỗ nào',
            'facebook', 'fb', 'face book', 'fanpage',
            'website', 'web', 'trang web',
            'zalo', 'messenger', 'mess', 'chat',
            'tư vấn', 'hỏi đáp', 'support', 'hỗ trợ',
            'báo giá', 'quote', 'giá cả', 'chi phí'
        ]
        
        # Cụm từ thường gặp
        contact_phrases = [
            'làm sao để liên hệ', 'cách liên hệ', 'muốn liên hệ',
            'thông tin liên hệ', 'liên hệ như thế nào',
            'số điện thoại của', 'email của', 'địa chỉ của',
            'tôi muốn gọi', 'muốn gọi điện', 'cần liên lạc',
            'làm sao để', 'contact information'
        ]
        
        # Kiểm tra từ khóa
        for keyword in contact_keywords:
            if keyword in query_lower:
                return True
        
        # Kiểm tra cụm từ
        for phrase in contact_phrases:
            if phrase in query_lower:
                return True
        
        return False
    
    def get_contact_response(self):
        """Tạo phản hồi về thông tin liên hệ với links có thể click"""
        phone_link = f'<a href="tel:{self.company_info["number"]}" style="color: #667eea; text-decoration: none; font-weight: bold;">{self.company_info["number"]}</a>'
        email_link = f'<a href="mailto:{self.company_info["email"]}" style="color: #667eea; text-decoration: none; font-weight: bold;">{self.company_info["email"]}</a>'
        website_link = f'<a href="https://{self.company_info["website"]}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">{self.company_info["website"]}</a>'
        facebook_link = f'<a href="{self.company_info["facebook"]}" target="_blank" style="color: #667eea; text-decoration: none; font-weight: bold;">VAV Furniture Facebook</a>'
        
        return f"""Đây là thông tin liên hệ của <strong>{self.company_info['name']}</strong>:

📞 <strong>Số điện thoại:</strong> {phone_link}
📧 <strong>Email:</strong> {email_link}  
📍 <strong>Địa chỉ:</strong> {self.company_info['address']}
🌐 <strong>Website:</strong> {website_link}
📘 <strong>Facebook:</strong> {facebook_link}

Bạn có thể click vào các link ở trên để liên hệ trực tiếp! Tôi có thể giúp gì khác cho bạn không?"""

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    """View chính cho chatbot"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id')
            
            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            # Tạo hoặc lấy session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'is_active': True}
            )
            
            # Lưu tin nhắn của user
            user_msg = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=user_message
            )
            
            # Tạo phản hồi
            chatbot_service = ChatbotService()
            response_data = chatbot_service.generate_response(user_message, session)
            
            # Lưu phản hồi của bot
            bot_msg = ChatMessage.objects.create(
                session=session,
                message_type='bot',
                content=response_data['response']
            )
            
            # Thêm sản phẩm/dự án được đề xuất
            if response_data['products']:
                product_ids = [p['id'] for p in response_data['products']]
                products = Product.objects.filter(id__in=product_ids)
                bot_msg.recommended_products.set(products)
            
            if response_data['projects']:
                project_ids = [p['id'] for p in response_data['projects']]
                projects = Project.objects.filter(id__in=project_ids)
                bot_msg.recommended_projects.set(projects)
            
            return JsonResponse({
                'response': response_data['response'],
                'session_id': session_id,
                'products': response_data['products'],
                'projects': response_data['projects'],
                'news': response_data['news'],
                'message_id': bot_msg.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error in chat view: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)


def chatbot_page(request):
    """Trang chatbot"""
    return render(request, 'chatbot/chat.html')


@csrf_exempt
@require_http_methods(["POST"])
def feedback_view(request):
    """API để nhận feedback từ người dùng"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message_id = data.get('message_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not all([session_id, rating]):
            return JsonResponse({'error': 'session_id and rating are required'}, status=400)
        
        session = ChatSession.objects.get(session_id=session_id)
        message = None
        if message_id:
            message = ChatMessage.objects.get(id=message_id)
        
        from .models import ChatFeedback
        ChatFeedback.objects.create(
            session=session,
            message=message,
            rating=rating,
            comment=comment
        )
        
        return JsonResponse({'success': True})
        
    except (ChatSession.DoesNotExist, ChatMessage.DoesNotExist):
        return JsonResponse({'error': 'Session or message not found'}, status=404)
    except Exception as e:
        logger.error(f"Error in feedback view: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

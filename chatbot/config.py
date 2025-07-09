"""
Cấu hình nâng cao cho Chatbot VAV Furniture
"""

# Cohere AI Settings
COHERE_SETTINGS = {
    'model': 'command-r-plus',  # Có thể thay đổi model
    'max_tokens': 1000,
    'temperature': 0.7,  # Độ sáng tạo (0-1)
    'k': 0,  # Top-k sampling
    'p': 0.75,  # Top-p sampling
}

# Chatbot Behavior Settings
CHATBOT_CONFIG = {
    # Số lượng tin nhắn gần đây được sử dụng làm context
    'context_messages': 10,
    
    # Số lượng sản phẩm/dự án tối đa trả về
    'max_recommendations': 5,
    
    # Số lượng items hiển thị trong widget (ít hơn để tiết kiệm không gian)
    'widget_max_items': 3,
    
    # Thời gian hiển thị notification badge (milliseconds)
    'notification_delay': 30000,
    
    # Tin nhắn chào mừng mặc định
    'welcome_message': """
Xin chào! Tôi là trợ lý ảo của VAV Furniture. Tôi có thể giúp bạn:
• Tìm kiếm sản phẩm nội thất
• Xem các dự án đã thực hiện  
• Tìm hiểu về quy trình thiết kế
• Đọc tin tức về nội thất
• Tư vấn thiết kế và lựa chọn sản phẩm

Bạn có câu hỏi gì cho tôi không?
""",
    
    # Tin nhắn lỗi mặc định
    'error_message': "Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau.",
    
    # Quick action buttons cho trang chatbot đầy đủ
    'quick_actions': [
        {
            'text': '🛋️ Tìm sofa',
            'message': 'Tôi muốn tìm hiểu về sản phẩm sofa'
        },
        {
            'text': '🏠 Dự án biệt thự', 
            'message': 'Cho tôi xem các dự án biệt thự'
        },
        {
            'text': '📋 Quy trình thiết kế',
            'message': 'Quy trình thiết kế của VAV như thế nào?'
        },
        {
            'text': '📰 Tin tức',
            'message': 'Tin tức mới nhất về nội thất'
        }
    ]
}

# Company Information Context
COMPANY_CONTEXT = {
    'name': 'VAV Furniture',
    'description': 'Công ty chuyên thiết kế và sản xuất nội thất cao cấp',
    'established': '2009',
    'experience': '15+ năm kinh nghiệm',
    
    'services': [
        'Thiết kế nội thất biệt thự',
        'Thiết kế nội thất căn hộ',
        'Thiết kế nội thất văn phòng', 
        'Thiết kế nội thất khách sạn',
        'Thiết kế nội thất nhà hàng',
        'Sản xuất đồ nội thất theo yêu cầu',
        'Tư vấn thiết kế miễn phí'
    ],
    
    'process_steps': [
        'Tư vấn & Thiết kế',
        'Lập kế hoạch & Vật liệu',
        'Sản xuất & Chế tác', 
        'Thi công & Lắp đặt',
        'Nghiệm thu & Bàn giao'
    ],
    
    'specialties': [
        'Nội thất gỗ tự nhiên cao cấp',
        'Thiết kế theo phong cách hiện đại',
        'Thiết kế theo phong cách cổ điển',
        'Nội thất thông minh, tiết kiệm không gian',
        'Thi công trọn gói từ A-Z'
    ],
    
    'contact_info': {
        'website': 'noithatvav.vn',
        'phone': '1900-xxxx',
        'email': 'info@noithatvav.vn',
        'address': 'Địa chỉ showroom VAV Furniture'
    }
}

# Search Keywords Mapping
SEARCH_KEYWORDS = {
    'products': {
        'sofa': ['sofa', 'ghế sofa', 'bộ sofa', 'ghế ngồi'],
        'table': ['bàn', 'bàn ăn', 'bàn làm việc', 'bàn coffee'],
        'bed': ['giường', 'giường ngủ', 'nệm', 'đầu giường'],
        'chair': ['ghế', 'ghế ăn', 'ghế làm việc', 'ghế thư giãn'],
        'cabinet': ['tủ', 'tủ quần áo', 'tủ bếp', 'kệ sách'],
        'decoration': ['đèn', 'tranh', 'gương', 'đồ trang trí']
    },
    
    'project_types': {
        'villa': ['biệt thự', 'villa', 'nhà biệt lập'],
        'apartment': ['căn hộ', 'chung cư', 'apartment'],
        'office': ['văn phòng', 'office', 'công ty'],
        'hotel': ['khách sạn', 'hotel', 'resort'],
        'restaurant': ['nhà hàng', 'restaurant', 'quán ăn', 'cafe']
    },
    
    'styles': {
        'modern': ['hiện đại', 'modern', 'tối giản', 'minimalist'],
        'classic': ['cổ điển', 'classic', 'vintage', 'retro'],
        'luxury': ['sang trọng', 'luxury', 'cao cấp', 'premium'],
        'industrial': ['công nghiệp', 'industrial', 'loft'],
        'scandinavian': ['scandinavian', 'bắc âu', 'nordic']
    }
}

# Response Templates
RESPONSE_TEMPLATES = {
    'product_found': "Tôi đã tìm thấy một số sản phẩm phù hợp với yêu cầu của bạn:",
    'project_found': "Dưới đây là một số dự án tham khảo cho bạn:",
    'news_found': "Đây là những tin tức liên quan:",
    'no_results': "Xin lỗi, tôi không tìm thấy kết quả phù hợp. Bạn có thể thử với từ khóa khác không?",
    'process_info': "Quy trình làm việc của VAV Furniture gồm 5 bước chính:",
    'contact_info': "Bạn có thể liên hệ với VAV Furniture qua:",
}

# Logging Configuration
CHATBOT_LOGGING = {
    'log_conversations': True,  # Có log cuộc trò chuyện không
    'log_search_queries': True,  # Có log các từ khóa search không
    'log_recommendations': True,  # Có log các gợi ý đã đưa ra không
    'log_feedback': True,  # Có log feedback không
}

# Analytics & Metrics
ANALYTICS_CONFIG = {
    'track_user_sessions': True,
    'track_popular_queries': True,
    'track_conversion_rate': True,  # Tỷ lệ click vào gợi ý
    'track_satisfaction_score': True,  # Điểm hài lòng từ feedback
}

# Performance Settings
PERFORMANCE_CONFIG = {
    'cache_responses': True,  # Cache các response phổ biến
    'cache_timeout': 3600,  # Cache trong 1 giờ
    'rate_limiting': {
        'enabled': True,
        'requests_per_minute': 60,  # Giới hạn 60 request/phút
        'requests_per_hour': 1000   # Giới hạn 1000 request/giờ
    }
}

# Security Settings  
SECURITY_CONFIG = {
    'filter_inappropriate_content': True,
    'max_message_length': 1000,
    'sanitize_input': True,
    'block_spam_patterns': True,
}

# Experimental Features (Có thể bật/tắt)
EXPERIMENTAL_FEATURES = {
    'voice_input': False,  # Nhập bằng giọng nói
    'image_upload': False,  # Upload hình ảnh để tư vấn
    'video_call_booking': False,  # Đặt lịch gọi video
    'live_agent_handoff': False,  # Chuyển sang nhân viên thật
    'multilingual_support': False,  # Hỗ trợ đa ngôn ngữ
}

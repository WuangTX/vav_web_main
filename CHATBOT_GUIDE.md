# Hướng dẫn Chatbot VAV Furniture

## Tổng quan

Chatbot VAV Furniture là một trợ lý ảo thông minh được tích hợp Cohere AI để hỗ trợ khách hàng:

- Tìm kiếm sản phẩm nội thất theo từ khóa
- Xem và tìm hiểu về các dự án đã thực hiện
- Đọc tin tức về nội thất và xu hướng thiết kế
- Tư vấn về quy trình thiết kế và lựa chọn sản phẩm
- Hiển thị sản phẩm/dự án gợi ý ngay trong chat
- Chuyển đến trang chi tiết khi click vào gợi ý

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Các package mới được thêm:
- `cohere==5.5.8` - Cohere AI SDK
- `channels==4.0.0` - Django Channels (cho WebSocket trong tương lai)
- `channels-redis==4.2.0` - Redis adapter cho Channels
- `redis==5.0.1` - Redis client

### 2. Cập nhật database

```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

### 3. Cấu hình API Key

Trong file `chatbot/views.py`, Cohere API key đã được cấu hình:
```python
COHERE_API_KEY = "44Mhomk58aaLnmrHPSXzc56vSsXtNjwtQwMZRGIa"
```

**Lưu ý bảo mật**: Trong production, nên chuyển API key vào environment variables:
```python
COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'your-default-key')
```

## Tính năng

### 1. Chatbot Widget (Floating)
- Hiển thị ở góc phải dưới mọi trang
- Interface nhỏ gọn, thân thiện
- Tự động hiện thông báo sau 30 giây
- Responsive trên mobile

### 2. Trang Chatbot đầy đủ
- Truy cập tại `/chatbot/`
- Interface rộng rãi hơn
- Hiển thị nhiều thông tin hơn
- Có các quick action buttons

### 3. Tính năng AI

#### Tìm kiếm thông minh
- Tìm sản phẩm theo tên, mô tả, danh mục
- Tìm dự án theo tiêu đề, loại, địa điểm
- Tìm tin tức theo tiêu đề, nội dung, tags

#### Hiển thị gợi ý
- Sản phẩm: Hiển thị tên, giá, danh mục, hình ảnh
- Dự án: Hiển thị tiêu đề, loại, địa điểm, hình ảnh  
- Tin tức: Hiển thị tiêu đề, danh mục, ngày đăng

#### Context-aware responses
- Chatbot hiểu ngữ cảnh cuộc trò chuyện
- Nhớ lịch sử chat gần đây
- Đưa ra câu trả lời phù hợp với thông tin công ty

### 4. Database Models

#### ChatSession
- Quản lý phiên chat của từng người dùng
- Lưu trữ session_id unique
- Có thể liên kết với User account

#### ChatMessage  
- Lưu trữ tất cả tin nhắn (user + bot)
- Liên kết với sản phẩm/dự án được đề xuất
- Hỗ trợ nhiều loại message (user, bot, system)

#### ChatFeedback
- Thu thập feedback từ người dùng
- Rating 1-5 sao cho từng phản hồi
- Comment text optional

## API Endpoints

### POST /chatbot/api/chat/
Gửi tin nhắn và nhận phản hồi

**Request:**
```json
{
    "message": "Tôi muốn tìm sofa da thật",
    "session_id": "uuid-string" // optional
}
```

**Response:**
```json
{
    "response": "Dựa trên yêu cầu của bạn...",
    "session_id": "uuid-string",
    "products": [...], // Array of matching products
    "projects": [...], // Array of matching projects  
    "news": [...],     // Array of matching news
    "message_id": 123
}
```

### POST /chatbot/api/feedback/
Gửi feedback cho phản hồi

**Request:**
```json
{
    "session_id": "uuid-string",
    "message_id": 123,
    "rating": 5,
    "comment": "Very helpful!" // optional
}
```

## Customization

### 1. Thay đổi prompt cho AI

Chỉnh sửa trong `ChatbotService.generate_response()`:

```python
context = f"""
Bạn là trợ lý ảo của công ty VAV Furniture...
[Tùy chỉnh prompt ở đây]
"""
```

### 2. Thêm loại gợi ý mới

1. Cập nhật models để thêm relationship mới
2. Thêm method search trong `ChatbotService`
3. Cập nhật template để hiển thị loại mới

### 3. Tùy chỉnh giao diện

**Widget:** Chỉnh sửa `templates/includes/chatbot_widget.html`
**Full page:** Chỉnh sửa `templates/chatbot/chat.html`

### 4. Thêm tính năng WebSocket (Tương lai)

Đã chuẩn bị sẵn Django Channels, có thể mở rộng để:
- Real-time messaging
- Typing indicators chính xác hơn
- Multi-user support
- Notifications

## Sử dụng

### Khách hàng có thể:

1. **Tìm sản phẩm:**
   - "Tôi muốn tìm sofa da thật"
   - "Có bàn ăn gỗ tự nhiên không?"
   - "Giá giường ngủ khoảng bao nhiêu?"

2. **Xem dự án:**
   - "Cho tôi xem dự án biệt thự"
   - "Có thiết kế nào cho căn hộ nhỏ không?"
   - "Dự án khách sạn mới nhất"

3. **Đọc tin tức:**
   - "Tin tức mới nhất về nội thất"
   - "Xu hướng thiết kế 2024"
   - "Cách chọn nội thất phù hợp"

4. **Tư vấn:**
   - "Quy trình thiết kế như thế nào?"
   - "Làm sao để chọn sofa phù hợp?"
   - "Chi phí thiết kế biệt thự"

### Click để xem chi tiết:
- Click vào sản phẩm gợi ý → Mở trang sản phẩm
- Click vào dự án gợi ý → Mở trang dự án  
- Click vào tin tức → Mở bài viết

## Admin Interface

Truy cập `/admin/` để quản lý:

- **Chat Sessions:** Xem danh sách phiên chat
- **Chat Messages:** Xem lịch sử tin nhắn
- **Chat Feedback:** Xem đánh giá từ khách hàng

## Troubleshooting

### Lỗi thường gặp:

1. **Cohere API không hoạt động:**
   - Kiểm tra API key
   - Kiểm tra kết nối internet
   - Xem logs trong console

2. **Không tìm thấy sản phẩm:**
   - Kiểm tra dữ liệu trong database
   - Thử search terms khác
   - Xem query trong admin

3. **Chatbot không phản hồi:**
   - Kiểm tra network request trong Dev Tools
   - Xem Django logs
   - Kiểm tra CSRF token

### Debug mode:

Thêm logging để debug:

```python
import logging
logger = logging.getLogger(__name__)

# Trong views.py
logger.error(f"Error details: {str(e)}")
```

## Cải tiến trong tương lai

1. **Voice Support:** Thêm speech-to-text/text-to-speech
2. **Image Recognition:** Nhận dạng hình ảnh sản phẩm
3. **Booking Integration:** Đặt lịch tư vấn trực tiếp
4. **Multi-language:** Hỗ trợ tiếng Anh
5. **Analytics:** Thống kê sử dụng chatbot
6. **CRM Integration:** Liên kết với hệ thống CRM

## Liên hệ hỗ trợ

Nếu có vấn đề kỹ thuật, vui lòng liên hệ team phát triển với thông tin:
- Error logs
- Steps to reproduce
- Browser/device information

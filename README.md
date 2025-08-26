# Recommendation Service v1

This project is the first phase of a recommendation system for a second-hand marketplace. It provides content-based recommendations using Elasticsearch's "More Like This" query and leverages Redis for caching.

## Getting Started

### Prerequisites

-   Python 3.x
-   Elasticsearch
-   Redis

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Navigate to the project directory:
    ```bash
    cd recommendation_service_v1
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file and add the following environment variables:
    ```
    ES_HOST=localhost
    ES_PORT=9200
    REDIS_HOST=localhost
    REDIS_PORT=6379
    FLASK_PORT=5000
    ```

### Running the Application

```bash
python app.py
```

## API Endpoint

### Get Recommendations

-   **URL:** `/api/v1/recommendations`
-   **Method:** `GET`
-   **Query Parameters:**
    -   `post_id` (required): The ID of the post to get recommendations for.
-   **Example Request:**
    ```
    http://localhost:5000/api/v1/recommendations?post_id=123
    ```

✦ Dưới đây là nhận xét của tôi về codebase của dự án này:

Codebase của dự án này có cấu trúc tốt và thể hiện sự hiểu biết rõ ràng về việc xây
dựng một hệ thống đề xuất dựa trên nội dung.

Dưới đây là phân tích của tôi:

Điểm mạnh:

-   Mục đích rõ ràng: Tệp README.md mô tả rõ ràng mục tiêu của dự án: hệ thống đề
    xuất dựa trên nội dung sử dụng Elasticsearch và Redis.
-   Thiết kế mô-đun: Việc tách biệt các mối quan tâm thành app.py (API),
    recommender/content_based.py (logic đề xuất) và utils/db_helpers.py (các hàm hỗ
    trợ cơ sở dữ liệu trong tương lai) giúp dễ dàng bảo trì.
-   Ngăn xếp công nghệ phù hợp: Flask, Elasticsearch và Redis là những lựa chọn thích  
    hợp cho loại ứng dụng này, mang lại hiệu suất và khả năng mở rộng tốt.
-   Bộ nhớ đệm hiệu quả: Việc triển khai bộ nhớ đệm Redis trong app.py được thực hiện  
    tốt, sử dụng các khóa bộ nhớ đệm rõ ràng và thời gian hết hạn hợp lý, điều này rất  
     quan trọng đối với hiệu suất.
-   Logic đề xuất cốt lõi: recommender/content_based.py sử dụng chính xác truy vấn
    "More Like This" của Elasticsearch, nhắm mục tiêu vào các trường liên quan
    (title, description, category).
-   Sử dụng biến môi trường: Việc sử dụng python-dotenv để cấu hình là một thực hành
    tốt.
-   Xử lý lỗi cơ bản: Mã bao gồm xử lý lỗi cơ bản cho các tham số bị thiếu và các vấn  
    đề kết nối.

Các lĩnh vực cần cải thiện/cân nhắc:

-   Xác thực đầu vào: Mặc dù post_id được kiểm tra sự hiện diện, nhưng việc xác thực
    mạnh mẽ hơn (ví dụ: kiểu, định dạng) sẽ nâng cao độ tin cậy của API.
-   Lập chỉ mục Elasticsearch: Dự án hiện thiếu mã để lập chỉ mục dữ liệu vào
    Elasticsearch. Đây là một phần quan trọng còn thiếu cho một hệ thống hoàn chỉnh.
-   Quản lý máy khách Elasticsearch: Trong recommender/content_based.py, một máy
    khách Elasticsearch mới được khởi tạo trong mỗi lần gọi. Để có hiệu suất tốt hơn
    trong môi trường sản xuất, hãy cân nhắc việc sử dụng lại một phiên bản máy khách
    duy nhất.
-   Ghi nhật ký: Việc báo cáo lỗi hiện tại sử dụng các câu lệnh print(). Việc triển
    khai một khung ghi nhật ký phù hợp (ví dụ: mô-đun logging của Python) sẽ có lợi
    cho việc giám sát và gỡ lỗi.
-   Kiểm thử: Không có tệp kiểm thử nào được cung cấp. Việc thêm các kiểm thử đơn vị
    và tích hợp sẽ cải thiện đáng kể chất lượng mã và đảm bảo tính đúng đắn.
-   `utils/db_helpers.py`: Tệp này hiện là một tệp giữ chỗ. Việc triển khai nó sẽ rất  
    quan trọng đối với bất kỳ tương tác cơ sở dữ liệu nào trong tương lai (ví dụ: tìm  
    nạp thông tin chi tiết bài đăng không có sẵn trong Elasticsearch).
-   Bảo mật: Đối với một hệ thống sản xuất, hãy cân nhắc thêm xác thực và ủy quyền
    vào điểm cuối API.

Kết luận:

Dự án này cung cấp một nền tảng vững chắc cho một hệ thống đề xuất dựa trên nội dung.  
 Nó được tổ chức tốt và sử dụng các công nghệ phù hợp. Việc giải quyết các lĩnh vực
cần cải thiện đã xác định, đặc biệt là liên quan đến lập chỉ mục Elasticsearch, quản
lý máy khách và kiểm thử, sẽ nâng cao đáng kể tính mạnh mẽ và khả năng sẵn sàng sản
xuất của nó.

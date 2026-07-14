# 1. Introduction

Tai nạn giao thông là một vấn đề nghiêm trọng ảnh hưởng đến an toàn công cộng trên toàn thế giới. Việc dự đoán mức độ nghiêm trọng của các vụ va chạm giao thông đóng vai trò quan trọng trong việc hỗ trợ các cơ quan chức năng đưa ra các biện pháp can thiệp kịp thời và phân bổ nguồn lực y tế hiệu quả. Mặc dù các phương pháp học máy (Machine Learning) truyền thống đã được áp dụng rộng rãi để dự đoán mức độ nghiêm trọng của tai nạn dựa trên các yếu tố về thời tiết, loại đường và tình trạng ánh sáng, các phương pháp này thường bỏ qua hoặc chưa khai thác tối đa thông tin không gian (ví dụ: tọa độ địa lý, độ phân giải địa lý của các cụm tai nạn).

Đặc biệt, rủi ro tử vong do tai nạn giao thông không phân bố đồng đều trên không gian. Các yếu tố như giới hạn tốc độ, khu vực đô thị hay nông thôn, và khoảng cách đến các cơ sở y tế thường có mối tương quan mạnh mẽ với vị trí xảy ra tai nạn. Tuy nhiên, các mô hình cơ sở thường không có các đặc trưng (features) đại diện trực tiếp cho yếu tố địa lý này. 

Bài báo này đề xuất một khung CatBoost được cải tiến với kỹ thuật đặc trưng không gian (Spatial Feature Engineering) để nâng cao khả năng dự đoán mức độ nghiêm trọng của tai nạn giao thông tại Vương quốc Anh (UK). Bằng cách khai thác thông tin từ vĩ độ (latitude) và kinh độ (longitude), hệ thống trích xuất các đặc trưng không gian quan trọng, đồng thời tận dụng khả năng xử lý biến phân loại (categorical variables) mạnh mẽ của CatBoost.

Câu hỏi nghiên cứu chính của bài báo là: Việc áp dụng kỹ thuật đặc trưng không gian (bao gồm phân cụm tọa độ và khoảng cách đến các thành phố lớn) có cải thiện hiệu suất dự đoán tử vong trong tai nạn giao thông của mô hình CatBoost so với các phương pháp học máy cơ sở hay không?

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Machine Learning | Học máy | Nhánh AI cho phép máy học từ dữ liệu mà không được lập trình tường minh. |
| Feature Engineering | Kỹ thuật đặc trưng | Quá trình sử dụng kiến thức lĩnh vực để tạo ra các đặc trưng giúp mô hình học máy hoạt động tốt hơn. |
| Categorical variables | Biến phân loại | Các biến chứa các giá trị là các danh mục, không mang tính thứ tự. |
| Latitude / Longitude | Vĩ độ / Kinh độ | Tọa độ địa lý để xác định vị trí trên bề mặt Trái Đất. |

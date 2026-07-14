# 2. Related Work

Các nghiên cứu trong tài liệu về mức độ nghiêm trọng và tử vong của tai nạn giao thông thường đánh giá các phương pháp tập hợp cây (tree-ensemble) và tăng cường (boosting) để so sánh với các mô hình tuyến tính cơ sở. Các mô hình này đã chứng minh được khả năng dự đoán đáng kể khi sử dụng các đặc trưng như điều kiện thời tiết, loại đường, tình trạng ánh sáng, và đặc điểm phương tiện. Tuy nhiên, việc mô hình hóa các yếu tố địa lý và không gian vẫn còn nhiều thách thức. Mặc dù các đặc trưng hiện có như giới hạn tốc độ (`speed_limit`) và khu vực đô thị hay nông thôn (`urban_or_rural_area`) có khả năng mã hóa gián tiếp một số khía cạnh không gian, nhưng chúng không cung cấp khái niệm trực tiếp về vị trí địa lý.

[CẦN BỔ SUNG: ít nhất 5 tài liệu tham khảo cụ thể về các nghiên cứu sử dụng học máy trong dự đoán mức độ nghiêm trọng của tai nạn giao thông và các ứng dụng của thông tin không gian trong lĩnh vực này, do sổ tay Jupyter gốc không chứa danh mục tài liệu tham khảo cụ thể.]

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Tree-ensemble | Tập hợp cây | Phương pháp kết hợp nhiều mô hình cây quyết định để tăng cường độ chính xác. |
| Boosting | Tăng cường | Phương pháp học máy tập hợp tạo ra một mô hình mạnh từ nhiều mô hình yếu tuần tự. |
| Baseline | Cơ sở | Mô hình tham chiếu dùng để so sánh hiệu suất với các mô hình phức tạp hơn. |

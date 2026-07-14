# 5. Discussion

Mức độ nghiêm trọng của tai nạn giao thông không đồng đều trên mặt không gian; nguy cơ tử vong chịu ảnh hưởng mạnh mẽ bởi các yếu tố có tính phân bố địa lý như phân bổ giới hạn tốc độ, đặc điểm vùng nông thôn so với thành thị, và khoảng cách đến các cơ quan phản ứng khẩn cấp. Mặc dù tập đặc trưng gốc đã gián tiếp mã hóa một phần thông tin này thông qua các biến như giới hạn tốc độ (`speed_limit`) hoặc phân loại khu vực (`urban_or_rural_area`), chúng thiếu vắng một khái niệm rõ ràng về vị trí địa lý cục bộ. 

Kỹ thuật đặc trưng không gian (Spatial Feature Engineering) được kỳ vọng lấp đầy khoảng trống này bằng cách cho phép mô hình học các tỷ lệ rủi ro cơ sở theo từng địa điểm cụ thể thông qua mã định danh cụm (`spatial_cluster`) hoặc nhận diện khoảng cách đến các trung tâm đô thị lớn (`dist_to_nearest_city_km`). Hơn nữa, việc sử dụng CatBoost với khả năng xử lý biến phân loại (categorical variables) bản địa thông qua số liệu thống kê mục tiêu (target statistics) về mặt lý thuyết rất phù hợp với các đặc trưng định danh không gian.

Tuy nhiên, bất chấp cơ sở lý thuyết vững chắc, kết quả thực nghiệm và phân tích tính thống kê (Bảng 2) cho thấy việc bổ sung các đặc trưng không gian không mang lại sự cải thiện có ý nghĩa về mặt dự đoán. Sự vắng mặt của cải thiện này có thể xuất phát từ hai nguyên nhân chính:
Thứ nhất, lượng dữ liệu bị thiếu tọa độ địa lý trong bộ dữ liệu khá lớn (chiếm khoảng 54%). Mặc dù nghiên cứu đã xử lý bằng giá trị cảnh giới (sentinel value) để tránh rò rỉ dữ liệu, việc thiếu hụt này làm loãng (dilute) tín hiệu học tập của các biến không gian, hạn chế đáng kể sức mạnh của chúng. 
Thứ hai, các biến cơ sở hiện tại (như `police_force`, `urban_or_rural_area`, `road_type`) có thể đã mã hóa các proxy (biến đại diện) không gian đủ tốt để dự đoán mức độ nghiêm trọng của tai nạn, khiến cho các cụm không gian bổ sung trở nên dư thừa.

Mặc dù hiệu suất tổng thể không tăng đáng kể, khung phân tích vẫn cung cấp một công cụ mạnh mẽ với tính ổn định cao và khả năng đánh giá một cách có hệ thống. Kết quả chỉ ra rằng trước khi đầu tư nhiều nguồn lực tính toán cho việc trích xuất và huấn luyện các biến không gian phức tạp, cần đảm bảo mức độ hoàn thiện của dữ liệu địa lý đầu vào.

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Spatial Feature Engineering | Kỹ thuật đặc trưng không gian | Việc trích xuất và biến đổi các thuộc tính liên quan đến không gian và vị trí địa lý. |
| Target statistics | Số liệu thống kê mục tiêu | Phương pháp mã hóa biến phân loại bằng cách tính toán giá trị trung bình của biến mục tiêu cho từng danh mục. |
| Sentinel value | Giá trị cảnh giới | Một giá trị đặc biệt được gán cho các điểm dữ liệu bị thiếu để phân biệt chúng. |
| Proxy | Biến đại diện | Một biến gián tiếp được sử dụng thay thế cho một biến khác không đo lường được trực tiếp. |

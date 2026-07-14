# 6. Conclusion

Bài báo này đã trình bày việc phát triển và đánh giá các mô hình học máy để dự đoán mức độ nghiêm trọng của các vụ tai nạn giao thông dựa trên dữ liệu từ Vương quốc Anh. Nghiên cứu đã đề xuất một khung phân loại CatBoost kết hợp với các kỹ thuật đặc trưng không gian nhằm nắm bắt các đặc tính rủi ro theo vị trí địa lý. 

Kết quả đánh giá trên 9 mô hình phân loại cho thấy các phương pháp học máy dựa trên kỹ thuật tăng cường độ dốc (Gradient Boosting) hiện đại, đặc biệt là CatBoost, XGBoost và LightGBM, vượt trội hơn hẳn so với các mô hình tuyến tính và cây quyết định cơ bản. Tuy nhiên, phân tích bóc tách và các kiểm định thống kê chuyên sâu đã chỉ ra rằng việc bổ sung các đặc trưng không gian không mang lại cải thiện đáng kể về mặt hiệu suất dự đoán. Điều này có thể được lý giải bởi giới hạn của chất lượng dữ liệu, đặc biệt là tỷ lệ bị thiếu dữ liệu tọa độ lên tới 54%, làm giảm đi khả năng phản ánh rủi ro không gian thực tế của mô hình.

Khuyến nghị được rút ra là trong công tác quản lý an toàn giao thông, mặc dù các mô hình GBDT mang lại độ chính xác cao trong việc xác định các tình huống va chạm có khả năng gây tử vong cao, việc đầu tư nâng cao chất lượng báo cáo dữ liệu không gian từ hiện trường tai nạn là yếu tố tiên quyết nếu muốn tận dụng lợi ích từ phân tích không gian.

Trong tương lai, các nghiên cứu tiếp theo có thể tập trung vào việc áp dụng phương pháp này trên các bộ dữ liệu có tọa độ địa lý đầy đủ hơn. Đồng thời, việc kết hợp thông tin không gian với các đặc trưng thời gian (temporal features) hoặc phân tích văn bản từ các báo cáo va chạm (textual crash reports) cũng hứa hẹn mang lại những cải tiến đột phá.

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Gradient Boosting | Tăng cường độ dốc | Kỹ thuật học máy xây dựng các mô hình dự đoán mạnh từ một tập hợp các mô hình dự đoán yếu hơn. |
| Temporal features | Đặc trưng thời gian | Các đặc tính liên quan đến thời gian xảy ra sự kiện, ví dụ như giờ, ngày, tháng. |
| Textual crash reports | Báo cáo va chạm dạng văn bản | Các ghi chép tự do mô tả diễn biến và hoàn cảnh của vụ tai nạn bằng văn bản. |

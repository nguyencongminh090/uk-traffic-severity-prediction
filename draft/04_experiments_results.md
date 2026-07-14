# 4. Experiments & Results

Nghiên cứu tiến hành đánh giá thực nghiệm trên 9 mô hình phân loại để xác định hiệu suất cơ sở, sau đó tiến hành phân tích bóc tách (ablation study) trên các biến thể của mô hình CatBoost để đánh giá tác động của kỹ thuật đặc trưng không gian.

## 4.1. Kết quả các Mô hình Cơ sở (Baseline Models)

Bảng 1 trình bày kết quả của 9 mô hình cơ sở được huấn luyện trên các đặc trưng ban đầu (chưa có đặc trưng không gian).

**Bảng 1**: So sánh hiệu suất của các mô hình cơ sở
| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) |
|---|---|---|---|---|---|---|
| CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 |
| XGBoost | 0.7358 | 0.7277 | 0.7537 | 0.7404 | 0.8130 | 16.48 |
| LightGBM | 0.7351 | 0.7262 | 0.7546 | 0.7401 | 0.8124 | 14.30 |
| Gradient Boosting | 0.7305 | 0.7194 | 0.7560 | 0.7372 | 0.8068 | 163.60 |
| Random Forest | 0.7300 | 0.7220 | 0.7480 | 0.7348 | 0.8066 | 121.81 |
| Extra Trees | 0.7150 | 0.7085 | 0.7305 | 0.7193 | 0.7883 | 62.29 |
| AdaBoost | 0.7115 | 0.7135 | 0.7067 | 0.7101 | 0.7873 | 55.98 |
| Decision Tree | 0.7156 | 0.7045 | 0.7425 | 0.7230 | 0.7839 | 3.23 |
| Logistic Regression | 0.6752 | 0.6834 | 0.6526 | 0.6677 | 0.7368 | 302.01 |

Kết quả cho thấy các mô hình GBDT hiện đại (CatBoost, XGBoost, LightGBM) vượt trội rõ rệt so với mô hình tuyến tính (Logistic Regression) với mức chênh lệch độ chính xác khoảng 6% và ROC-AUC khoảng 0.08. CatBoost đạt kết quả cao nhất với ROC-AUC là 0.8132.

Độ ổn định của các mô hình cũng được kiểm chứng qua kỹ thuật kiểm tra chéo 5 lần (5-Fold Cross Validation). ROC-AUC của CatBoost đạt 0.8119 ± 0.0019, khẳng định tính ổn định của mô hình.

## 4.2. Phân tích Bóc tách (Ablation Study)

Để đánh giá riêng lẻ sự đóng góp của kỹ thuật đặc trưng không gian và các cải tiến trong huấn luyện, Bảng 2 trình bày kết quả phân tích bóc tách với ba biến thể của CatBoost.

**Bảng 2**: Phân tích bóc tách các biến thể CatBoost
| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time (s) |
|---|---|---|---|---|---|---|
| 1. Baseline CatBoost | 0.7360 | 0.7271 | 0.7555 | 0.7410 | 0.8132 | 41.88 |
| 2. CatBoost + Spatial Features | 0.7350 | 0.7262 | 0.7542 | 0.7400 | 0.8132 | 169.05 |
| 3. Final Improved CatBoost | 0.7362 | 0.7278 | 0.7547 | 0.7410 | 0.8136 | 279.67 |

Đáng chú ý, kết quả thực nghiệm cho thấy việc bổ sung các đặc trưng không gian (Mô hình 2) và kết hợp tinh chỉnh tham số (Mô hình 3) chỉ mang lại sự gia tăng rất nhỏ về mặt chỉ số. Cụ thể, ROC-AUC tăng từ 0.8132 lên 0.8136 ở mô hình cuối cùng. Tuy nhiên, thời gian huấn luyện tăng lên đáng kể (từ 41.88 giây lên 279.67 giây).

## 4.3. Phân tích Tính Thống kê

Kiểm định McNemar (McNemar's Test) so sánh các dự đoán của mô hình CatBoost cơ sở và mô hình CatBoost cải tiến cuối cùng trên cùng tập kiểm tra. Kết quả cho thấy 795 trường hợp chỉ mô hình cơ sở dự đoán đúng, trong khi 808 trường hợp chỉ mô hình cải tiến dự đoán đúng (chi-square = 0.0898, p-value = 0.7644). Hơn nữa, kiểm định t-test bắt cặp (Paired t-test) trên điểm ROC-AUC của quá trình kiểm tra chéo cũng cho kết quả không có ý nghĩa thống kê (p = 0.3099). Do đó, sự cải thiện từ các đặc trưng không gian trong nghiên cứu này không có ý nghĩa thống kê ở mức 0.05.

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Baseline Models | Các mô hình cơ sở | Các mô hình phân loại được sử dụng làm mốc so sánh ban đầu. |
| Cross Validation | Kiểm tra chéo | Kỹ thuật đánh giá mô hình bằng cách chia dữ liệu thành nhiều tập con (folds) luân phiên làm tập huấn luyện và kiểm tra. |
| Ablation study | Phân tích bóc tách | Quá trình loại bỏ hoặc thêm dần các thành phần của mô hình để đánh giá đóng góp của từng thành phần. |
| McNemar's Test | Kiểm định McNemar | Kiểm định thống kê dùng cho dữ liệu danh mục bắt cặp để so sánh sự khác biệt giữa hai mô hình phân loại. |
| Paired t-test | Kiểm định t-test bắt cặp | Kiểm định thống kê để so sánh trung bình của hai mẫu có liên quan. |

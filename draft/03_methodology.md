# 3. Methodology

## 3.1. Dữ liệu và Tiền xử lý

Nghiên cứu sử dụng tập dữ liệu tai nạn tại Vương quốc Anh, được lưu trữ trong tệp `UK_accidents_balanced.csv`. Bộ dữ liệu ban đầu bao gồm 289.444 mẫu (rows) và 44 đặc trưng (columns). 

Biến mục tiêu (target variable) ban đầu là `collision_severity` chứa ba nhãn (1: Fatal, 2: Serious, 3: Slight). Để phục vụ cho bài toán phân loại nhị phân, các nhãn 2 và 3 được gộp thành nhãn 0 (Non-Fatal). Sau khi chuyển đổi, tập dữ liệu đạt trạng thái cân bằng hoàn hảo với 144.722 mẫu cho nhãn Fatal (1) và 144.722 mẫu cho nhãn Non-Fatal (0).

Quá trình tiền xử lý (preprocessing) bao gồm các bước:
1. **Loại bỏ đặc trưng gây rò rỉ và đặc trưng định danh (Leak and ID columns)**: Các cột như `enhanced_severity_collision`, `collision_injury_based`, `collision_index`, v.v. được loại bỏ để ngăn chặn hiện tượng rò rỉ dữ liệu (data leakage).
2. **Xử lý dữ liệu bị thiếu (Missing values)**: Các biến số (numerical variables) được điền bằng giá trị trung vị (median), trong khi các biến phân loại (categorical variables) được điền bằng nhãn "missing".
3. **Mã hóa nhãn (Label Encoding)**: Các biến phân loại sau đó được mã hóa bằng `LabelEncoder`.
4. **Phân chia tập dữ liệu**: Tập dữ liệu được chia thành tập huấn luyện (train set) với 231.555 mẫu và tập kiểm tra (test set) với 57.889 mẫu theo tỷ lệ 80:20, có phân tầng (stratify) theo biến mục tiêu.

```python
# Tiền xử lý biến mục tiêu (Target)
df_model[TARGET] = df_model[TARGET].replace({2: 0, 3: 0})

# Phân chia tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
```

## 3.2. Kỹ thuật Đặc trưng Không gian (Spatial Feature Engineering)

Để nắm bắt ảnh hưởng của vị trí địa lý đối với mức độ nghiêm trọng của tai nạn, nghiên cứu áp dụng kỹ thuật đặc trưng không gian trên các biến `latitude` (vĩ độ) và `longitude` (kinh độ). Đáng chú ý, khoảng 54% mẫu có tọa độ bị thiếu. Thay vì sử dụng các kỹ thuật điền khuyết có thể gây sai lệch phân phối không gian, các mẫu này được gán một giá trị cảnh giới (sentinel value) rõ ràng là `-1` hoặc `"unknown"`. 

Các đặc trưng không gian được tạo ra bao gồm:
- `spatial_cluster`: Mã định danh cụm địa lý được tạo bằng thuật toán KMeans (k=20) trên tọa độ. (Thuật toán KMeans chỉ được huấn luyện trên tập huấn luyện để tránh rò rỉ dữ liệu).
- `grid_region_id`: Mã định danh ô lưới tĩnh kích thước 0.5°×0.5° vĩ độ/kinh độ.
- `cluster_density`: Tỷ lệ các mẫu huấn luyện rơi vào cùng một cụm không gian, đại diện cho mức độ đông đúc/mật độ của khu vực.
- `dist_to_nearest_city_km` và `nearest_city_zone`: Khoảng cách Haversine (km) đến thành phố gần nhất trong số 8 thành phố lớn của Vương quốc Anh, và tên của vùng thành phố đó.

## 3.3. Các Mô hình Đánh giá Cơ sở

Nghiên cứu đánh giá 9 mô hình phân loại phổ biến trong lĩnh vực dự đoán tai nạn giao thông:
- Tuyến tính: Logistic Regression
- Cây đơn: Decision Tree
- Tập hợp Bagging: Random Forest, Extra Trees
- Tăng cường (Boosting) cổ điển: AdaBoost, Gradient Boosting
- GBDT hiện đại: XGBoost, LightGBM, CatBoost

## 3.4. Khung CatBoost Cải tiến

Trong số các mô hình trên, mô hình CatBoost được chọn để phát triển khung cải tiến. Quy trình cải thiện hiệu suất của CatBoost tập trung vào các tính năng bản địa của thư viện:
- Xử lý trực tiếp các biến phân loại thông qua tham số `cat_features`, sử dụng số liệu thống kê mục tiêu (target statistics) thay vì mã hóa số nguyên đơn thuần.
- Sử dụng tập kiểm định (validation set) lấy 15% từ tập huấn luyện.
- Áp dụng kỹ thuật dừng sớm (early stopping) với ngưỡng 50 vòng (rounds) để chống quá khớp (overfitting).
- Tinh chỉnh siêu tham số nhẹ nhàng trên các tham số `depth`, `learning_rate`, và `l2_leaf_reg`.

## 3.5. Chỉ số Đánh giá (Evaluation Metrics)

Hiệu suất của các mô hình được đánh giá thông qua các chỉ số: Độ chính xác (Accuracy), Độ nhạy (Recall), Độ chuẩn xác (Precision), Điểm F1-Macro, Ma trận nhầm lẫn (Confusion Matrix), và Diện tích dưới đường cong đặc trưng hoạt động (ROC-AUC). Ngoài ra, thời gian huấn luyện và thời gian suy luận cũng được đo lường để đánh giá sự đánh đổi (trade-off) giữa độ chính xác và chi phí tính toán.

## Thuật ngữ (Glossary)
| Thuật ngữ (EN) | Tương đương (VN) | Định nghĩa ngắn |
|---|---|---|
| Target variable | Biến mục tiêu | Biến mà mô hình học máy cần dự đoán. |
| Data leakage | Rò rỉ dữ liệu | Hiện tượng mô hình học máy sử dụng thông tin từ tập kiểm tra hoặc tương lai trong quá trình huấn luyện. |
| Missing values | Dữ liệu bị thiếu | Các giá trị không được ghi nhận hoặc không có sẵn trong bộ dữ liệu. |
| Numerical variables | Biến số | Biến có giá trị là các con số định lượng. |
| Train/Test set | Tập huấn luyện/Tập kiểm tra | Các phần của bộ dữ liệu dùng để huấn luyện và đánh giá mô hình. |
| Sentinel value | Giá trị cảnh giới | Một giá trị cụ thể được sử dụng để biểu thị sự vắng mặt của dữ liệu hợp lệ. |
| Stratify | Phân tầng | Kỹ thuật lấy mẫu đảm bảo tỷ lệ phân phối của biến mục tiêu được giữ nguyên ở các tập dữ liệu. |
| Early stopping | Dừng sớm | Kỹ thuật dừng huấn luyện khi hiệu suất trên tập kiểm định không còn cải thiện. |
| Overfitting | Quá khớp | Tình trạng mô hình học máy hoạt động quá tốt trên tập huấn luyện nhưng kém trên dữ liệu mới. |
| Confusion Matrix | Ma trận nhầm lẫn | Bảng tóm tắt kết quả phân loại của mô hình, hiển thị các dự đoán đúng và sai. |
| ROC-AUC | Diện tích dưới đường cong ROC | Chỉ số đo lường hiệu suất tổng thể của mô hình phân loại nhị phân ở các ngưỡng khác nhau. |

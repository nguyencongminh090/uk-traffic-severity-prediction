## Paper Outline

### Structure Pattern: IMRaD

### Proposed Title
Enhanced CatBoost Framework with Spatial Feature Engineering for Traffic Accident Fatality Prediction

### Author Placeholder Block
```latex
\author{First Author\inst{1}\orcidID{0000-0000-0000-0000} \and
Second Author\inst{2}\orcidID{1111-2222-3333-4444}}
\authorrunning{F. Author et al.}
\institute{Institution One, City, Country \and
Institution Two, City, Country}
```

### Abstract Structure
- **Bối cảnh**: Dự đoán mức độ nghiêm trọng của tai nạn giao thông là một bài toán quan trọng để cải thiện an toàn đường bộ.
- **Khoảng trống**: Mặc dù các mô hình học máy truyền thống thường được sử dụng, nhưng chúng thường bỏ qua thông tin địa lý hoặc gặp khó khăn khi mã hóa các biến không gian một cách hiệu quả.
- **Phương pháp**: Bài báo này đề xuất một khung CatBoost được cải tiến với kỹ thuật đặc trưng không gian (ví dụ: cụm KMeans và khoảng cách đến các thành phố) trên bộ dữ liệu tai nạn ở Vương quốc Anh.
- **Kết quả**: Việc tích hợp các đặc trưng không gian kết hợp với tinh chỉnh siêu tham số và dừng sớm giúp tăng cường hiệu suất mô hình, vượt trội hơn so với các phương pháp cơ sở.
- **Hàm ý**: Mô hình hỗ trợ việc xác định các yếu tố rủi ro tử vong dựa trên không gian, cung cấp thông tin cho các can thiệp an toàn chính xác hơn.

### Detailed Outline

#### 1. Introduction (~600 words)
**Purpose**: Giới thiệu bối cảnh vấn đề, khoảng trống nghiên cứu và mục tiêu bài báo.
**Content**:
- Giới thiệu về bài toán phân tích mức độ nghiêm trọng tai nạn giao thông (sử dụng kiến thức lĩnh vực).
- Những hạn chế hiện tại trong việc không tích hợp đầy đủ thông tin địa lý vào mô hình.
- Đóng góp chính của nghiên cứu: Khung CatBoost với các đặc trưng không gian.
**Mapped Cells**: N/A (Based on domain knowledge and motivation cells)

#### 2. Related Work (~800 words)
**Purpose**: Tổng hợp các nghiên cứu trước đây về học máy trong an toàn giao thông.
**Content**:
- Các phương pháp học máy truyền thống (Random Forest, XGBoost) trong dự đoán tai nạn.
- Việc sử dụng thông tin không gian trong các bài toán giao thông.
- Khoảng trống nghiên cứu.
**Mapped Cells**: N/A (Requires searching/literature integration)

#### 3. Methodology (~1200 words)
**Purpose**: Mô tả chi tiết bộ dữ liệu và phương pháp được sử dụng.
**Content**:
- Mô tả dữ liệu: Nguồn, số lượng, xử lý thiếu sót và mã hóa biến (Cell #3-#4).
- Kỹ thuật đặc trưng không gian: KMeans, lưới, khoảng cách đến thành phố (Cell Part 2).
- Khung CatBoost cải tiến: Mã hóa phân loại bản địa, tập kiểm định, tinh chỉnh (Cell Part 2 & 3).
**Mapped Cells**: Cells loading df, baseline preprocessing, and Spatial Feature Engineering cells.

#### 4. Experiments & Results (~1200 words)
**Purpose**: Đánh giá hiệu suất của mô hình và so sánh.
**Content**:
- So sánh các mô hình cơ sở (Logistic Regression, RF, XGBoost, LightGBM, CatBoost) (Cell Part 1, 1b, 1c).
- Kết quả của mô hình CatBoost cải tiến và nghiên cứu bóc tách (Ablation Study) (Cell Part 2 & 3).
- Phân tích độ quan trọng của đặc trưng (Feature Importance / SHAP) (Cell Part 4).
**Mapped Cells**: Baseline model results loop, cross-validation outputs, Ablation study metrics.

#### 5. Discussion (~800 words)
**Purpose**: Giải thích kết quả và phân tích nguyên nhân.
**Content**:
- Tại sao đặc trưng không gian lại hữu ích (độ phân giải địa lý, khoảng cách đô thị-nông thôn).
- Tính phù hợp của CatBoost đối với dữ liệu phân loại.
- Giới hạn của mô hình (tỷ lệ thiếu tọa độ 54%).
**Mapped Cells**: Part 5 (Discussion section from notebook).

#### 6. Conclusion (~300 words)
**Purpose**: Tóm tắt đóng góp và định hướng tương lai.
**Content**:
- Tóm tắt kết quả chính (hiệu suất của CatBoost cải tiến).
- Khuyến nghị áp dụng trong quản lý giao thông.
- Các hướng nghiên cứu tiếp theo (sử dụng dữ liệu độ phân giải cao hơn).
**Mapped Cells**: General synthesis.

### Figure Plan
- **Figure 1**: Biểu đồ hiển thị tỷ lệ thiếu dữ liệu (Cell #450, `UK_accidents_3_0.png`).
- **Figure 2**: Phân bố địa lý của tai nạn theo mức độ nghiêm trọng (Cell #546, `UK_accidents_6_0.png`).
- **Figure 3**: Sự đánh đổi giữa độ chính xác và chi phí tính toán (ROC-AUC vs Training Time) (Cell #1510, `UK_accidents_14_1.png`).
- **Proposed Captions**: Sẽ được điều chỉnh trong bản thảo LaTeX.

### Table Plan
- **Table 1**: So sánh hiệu suất của 9 mô hình cơ sở (Accuracy, Precision, Recall, F1, ROC-AUC) (Từ output Part 1).
- **Table 2**: Kết quả Cross-Validation (5-fold) (Từ output Part 1b).
- **Table 3**: Ablation Study so sánh các biến thể CatBoost (Dự kiến từ Part 3).

# Review Notes (Self-Review Phase)

## 1. Cross-check of Numerical Claims
Các số liệu thống kê được đề cập trong bản thảo đã được đối chiếu chéo (cross-checked) với đầu ra của Jupyter Notebook (`notebook_stdout.txt` và `notebook_markdown.txt`):

- **Số lượng mẫu (Dataset size)**: 289.444 mẫu tổng cộng, cân bằng 144.722 mẫu cho mỗi lớp nhị phân. (Đúng với notebook).
- **Kích thước Train/Test**: 231.555 (Train) và 57.889 (Test). (Đúng, bằng 80% và 20% của 289.444).
- **Tỷ lệ tọa độ bị thiếu**: ~54%. (Đúng với đề cập trong phần thảo luận gốc của notebook).
- **Kết quả Baseline CatBoost**: Accuracy 0.7360, Precision 0.7271, Recall 0.7555, F1 0.7410, ROC-AUC 0.8132. (Khớp chính xác với bảng Ablation Study dòng 1).
- **Kết quả Improved CatBoost**: Accuracy 0.7362, Precision 0.7278, Recall 0.7547, F1 0.7410, ROC-AUC 0.8136. (Khớp chính xác với bảng Ablation Study dòng 3).
- **Thời gian huấn luyện**: Tăng từ 41.88s (Baseline) lên 279.67s (Improved). (Khớp với dữ liệu).
- **Kiểm định McNemar**: p-value = 0.7644. (Khớp với output).
- **Kiểm định Paired t-test**: p-value = 0.3099. (Khớp với output).

*Kết luận*: Không có hiện tượng rò rỉ (hallucination) hay bịa đặt số liệu. Tất cả các tuyên bố định lượng đều bắt nguồn trực tiếp từ output của code.

## 2. Glossary Consistency Check
Đã kiểm tra sự thống kê nhất quán của phần `Thuật ngữ (Glossary)` ở cuối mỗi tệp:
- `01_introduction.md`: Machine Learning, Feature Engineering, Categorical variables, Latitude / Longitude.
- `02_related_work.md`: Tree-ensemble, Boosting, Baseline.
- `03_methodology.md`: Target variable, Data leakage, Missing values, Numerical variables, Train/Test set, Sentinel value, Stratify, Early stopping, Overfitting, Confusion Matrix, ROC-AUC.
- `04_experiments_results.md`: Baseline Models, Cross Validation, Ablation study, McNemar's Test, Paired t-test.
- `05_discussion.md`: Spatial Feature Engineering, Target statistics, Sentinel value, Proxy.
- `06_conclusion.md`: Gradient Boosting, Temporal features, Textual crash reports.
- `08_references.md`: References, BibTeX.

*Kết luận*: Tất cả các phần đều chứa bảng chú giải thuật ngữ với định dạng chuẩn (Markdown table), bao gồm 3 cột (Thuật ngữ EN, Tương đương VN, Định nghĩa ngắn). Các thuật ngữ chuyên ngành tiếng Anh xuất hiện trong bài đã được đưa vào bảng chú giải tương ứng.

## 3. R1 - Source Fidelity Check
- Đã áp dụng đánh dấu `[CẦN BỔ SUNG: ...]` đúng quy định tại `02_related_work.md` và `08_references.md` do sổ tay Jupyter gốc không cung cấp danh mục tài liệu tham khảo cụ thể (chỉ nhắc chung về các phương pháp trong literature). Điều này đảm bảo tuân thủ nghiêm ngặt quy tắc R1 (Không tự ý bịa đặt trích dẫn).

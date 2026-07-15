# 📅 Hệ Thống Giải Toán Tối Ưu Phân Công Giám Thị (IAP Solver)

Dự án này triển khai mô hình Quy hoạch Tuyến tính Nguyên(ILP - Integer Linear Programming) giải quyết bài toán **Invigilator Assignment Problem (IAP)**. Hệ thống tự động hóa quá trình phân bổ cán bộ coi thi vào các ca thi dựa trên dữ liệu thực tế, cân đối giữa nguyện vọng địa lý (Cơ sở làm việc) và tính công bằng về khối lượng công việc (Workload Fairness).

---

## 🚀 Tính Năng Chính Của Hệ Thống

- **Tiền xử lý dữ liệu thực tế (`preprocess_real_data`):** Tự động đọc file cấu trúc Excel, nhận diện danh sách cán bộ, ca thi, tính toán nhu cầu nhân lực (`demand`) và lọc các cặp ca bị trùng lịch thi.
- **Mô hình tối ưu hóa toán học (`solve_iap_model`):** Định biên tối ưu sử dụng thư viện `PuLP` và bộ giải `CBC` mã nguồn mở.
- **Phân tích đa mục tiêu & Nới lỏng ràng buộc (`run_tuning_and_relaxation`):** Khảo sát biên Pareto thông qua Grid Search với 3 kịch bản trọng số khác nhau. Tích hợp biến lỏng (Slack Variables) và phạt Big-M chống trạng thái vô nghiệm (Infeasible).
- **Đánh giá hiệu năng hệ thống (`run_performance_benchmark`):** So sánh đối sánh định lượng các chỉ số thống kê (Max/Min tải, độ lệch chuẩn, chi phí di chuyển) giữa phương án tối ưu ILP và lịch lịch phân công thủ công ban đầu (Baseline).

---

## 🛠️ Yêu Cầu Hệ Thống & Cài Đặt

### 1. Yêu cầu môi trường

- **Python**: Phiên bản `3.10` trở lên.
- **Hệ điều hành**: Windows, macOS hoặc Linux.

### 2: Kích hoạt môi trường ảo (Virtual Environment)

Để đảm bảo chương trình chạy với đầy đủ các thư viện đã cài đặt sẵn trong môi trường ảo `venv`, hãy mở Terminal / Command Prompt tại thư mục chứa dự án và gõ lệnh kích hoạt:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Cài đặt các thư viện phụ thuộc

Mở Terminal / Command Prompt tại thư mục chứa dự án và chạy lệnh sau để cài đặt các gói thư viện cần thiết:

```powershell
pip install pandas pulp numpy openpyxl
```

### 4. Khởi chạy chương trình

Đảm bảo file dữ liệu Excel Dataset_Anonymized_Invigilator_Assignment_Problem.xlsx đã nằm chung thư mục với file code. Tiến hành chạy chương trình bằng lệnh:

```powershell
python IAP_Solver.py
```

Lưu ý để code chạy hiệu quả nên chạy 2 lần cho lần đầu chạy code

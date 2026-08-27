# 📊 Bộ Công Cụ Tạo Excel Fanpage Reels v2.0

Ứng dụng Desktop (Giao diện trực quan Tkinter) hỗ trợ tự động quét kho video thành phẩm, kết hợp danh sách Page/UID và tạo file Excel biểu mẫu đăng bài Reels hàng loạt lên Facebook.

---

## 🌟 Các Tính Năng Chính

1. **Quét Kho Video Thông Minh**:
   - Tự động duyệt qua các thư mục video thành phẩm.
   - Bỏ qua các file phụ (như `video-9x16.mp4`) để lấy đúng file video render chuẩn.
   - Tự động lấy tiêu đề bài viết từ file `link-da-dang.txt` hoặc trích xuất làm sạch từ tên file / tên folder.

2. **Lọc Domain Bình Luận Chính Xác**:
   - Nhập tên miền (ví dụ: `danhngon.pro`, `nextpart2.online`) để tool tự động trích xuất đúng link bài viết chứa domain đó trong file `link-da-dang.txt` để đưa vào cột `Bình luận đầu tiên`.

3. **Tùy Chọn Phân Bổ Page / Video**:
   - Hỗ trợ chọn tỷ lệ phân bổ từ 1 đến 3 Page trên mỗi video.
   - Tự động xuất file `page-chua-dang.txt` chứa danh sách các Page còn dư nếu số lượng Page nhiều hơn số video trong kho.

4. **Hỗ Trợ 2 Định Dạng File Excel Chuẩn**:
   - **File Excel Thường (11 cột)**: `STT | Trang | Nền tảng | Loại bài | Nội dung | URL video/ảnh | Bình luận đầu tiên | Ngày đăng | Giờ đăng | Múi giờ | Hành động`.
   - **File Excel Token (12 cột có UID)**: `STT | Trang | UID | Nền tảng | Loại bài | Nội dung | URL video/ảnh | Bình luận đầu tiên | Ngày đăng | Giờ đăng | Múi giờ | Hành động`.

5. **Ghi Nhớ Cấu Hình & Lịch Sử**:
   - Ghi nhớ các đường dẫn thư mục, hashtag, tên miền đã nhập từ phiên làm việc trước.
   - Ghi nhớ folder video cuối cùng đã sử dụng để tránh lấy trùng lặp ở các đợt tạo Excel tiếp theo.

---

## 🚀 Hướng Dẫn Sử Dụng

### Cách 1: Chạy trực tiếp qua file Batch
Nhấp đúp vào file `Chay_Tool.bat` trong thư mục dự án.

### Cách 2: Chạy bằng mã nguồn Python
```bash
pip install openpyxl
python main.py
```

### Cách 3: Đóng gói thành file `.exe`
Chạy file `build_exe.bat` để biên dịch ứng dụng thành file `.exe` trong thư mục `dist/`.

---

## 🏗️ Cấu Trúc Mã Nguồn

- `main.py`: Điểm khởi chạy ứng dụng Tkinter GUI.
- `ui_builder.py` / `ui.py`: Xây dựng bố cục giao diện người dùng.
- `app_controller.py`: Xử lý luồng nghiệp vụ, kiểm tra dữ liệu và điều phối tạo file.
- `core.py`: Quét kho video, đọc file text và phân tích dữ liệu.
- `excel_writer.py`: Định dạng, tạo sheet `BaiDang`, căn chỉnh độ rộng cột và xuất file Excel.
- `config_mgr.py`: Lưu và nạp cấu hình người dùng.
- `worker.py`: Xử lý đa luồng (Background Worker) giúp giao diện không bị đơ/lag khi xử lý lượng lớn video.

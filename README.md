# Đồ án Môn học: Cấu trúc Dữ liệu và Giải thuật (IT003)
## Đề tài: Phát triển Game 2048 cơ bản

### 👤 Thông tin sinh viên
- **Họ và tên:** Lê Trịnh Quỳnh Như
- **Mã sinh viên:** 25521343
- **Lớp:** IT003.Q21.TTNT

### 🎮 Tính năng ứng dụng
- **Cơ chế Game:** Logic 2048 chuẩn với hiệu ứng trượt (Animation).
- **Cấu trúc dữ liệu Stack:** Tính năng **Undo (Hoàn tác)** không giới hạn bước, lưu trữ trạng thái bàn chơi và điểm số.
- **Xử lý Thắng/Thua:** Tự động kiểm tra trạng thái game sau mỗi nước đi.
- **Giao diện:** Đồ họa Pygame trực quan, màu sắc chuẩn bản gốc.

### 🛠 Cấu trúc thư mục
- `main.py`: Nhạc trưởng điều khiển vòng lặp game và xử lý sự kiện.
- `logic.py`: Chứa các thuật toán xử lý mảng, logic gộp ô và quản lý Stack.
- `constant.py`: Định nghĩa các hằng số màu sắc, kích thước và font chữ.

### 🚀 Hướng dẫn khởi chạy
1. Cài đặt thư viện: `pip install pygame`
2. Chạy game: `python3 main.py`
3. Phím tắt: Các phím mũi tên để di chuyển, phím **U** hoặc nút bấm trên màn hình để **Undo**.

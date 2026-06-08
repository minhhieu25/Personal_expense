# Personal Finance Manager (Quản Lý Chi Tiêu Cá Nhân)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

Một ứng dụng web được xây dựng bằng Django giúp người dùng dễ dàng theo dõi, quản lý chi tiêu, thiết lập ngân sách và kiểm soát dòng tiền cá nhân một cách trực quan và hiệu quả.

---

## 🚀 Công nghệ sử dụng (Tech Stack)
- **Backend:** Python, Django Framework, Django REST Framework
- **Database:** PostgreSQL
- **Xử lý đa phương tiện:** Pillow (Image Processing)
- **Frontend:** HTML5, CSS3 (Modern UI/UX với Dark/Light Mode), JavaScript (Vanilla)

---

## ⚙️ Yêu cầu hệ thống (Prerequisites)
Đảm bảo máy tính của bạn đã cài đặt các phần mềm sau trước khi chạy dự án:
- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)

---

## 🛠 Hướng dẫn Cài đặt & Khởi chạy (Installation & Setup)

Làm theo các bước dưới đây để cài đặt và chạy dự án trên môi trường Local:

### Bước 1: Khởi tạo Môi trường Ảo (Virtual Environment)
Việc sử dụng môi trường ảo giúp cô lập các thư viện của dự án, tránh xung đột hệ thống.
```bash
python -m venv venv
```
Kích hoạt môi trường ảo (trên Windows):
```bash
venv\Scripts\activate
```
*(Trên macOS/Linux: `source venv/bin/activate`)*

### Bước 2: Cài đặt Thư viện Phụ thuộc (Dependencies)
Cài đặt các gói phần mềm cần thiết trực tiếp thông qua `pip`:
```bash
pip install django
pip install psycopg2-binary
pip install djangorestframework
pip install Pillow
```
*(Lưu ý: Bạn cũng có thể gom chung vào lệnh `pip install django psycopg2-binary djangorestframework Pillow`)*

### Bước 3: Khởi tạo Cơ sở Dữ liệu (Database Migration)
Áp dụng các thay đổi cấu trúc bảng (schema) vào trong Database:
```bash
python manage.py migrate
```

### Bước 4: Khởi tạo Tài khoản Quản trị (Superuser)
Tạo tài khoản để truy cập vào trang Admin của hệ thống:
```bash
python manage.py createsuperuser
```
*(Làm theo hướng dẫn trên màn hình để nhập Username, Email, và Password)*

### Bước 5: Khởi chạy Máy chủ (Run Server)
Bật máy chủ phát triển (Development Server):
```bash
python manage.py runserver
```

Truy cập ứng dụng trên trình duyệt qua địa chỉ: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 💡 Lưu ý (Notes)
- Hãy đảm bảo bạn đã cấu hình chuỗi kết nối Database chuẩn xác trong file `settings.py` để PostgreSQL có thể hoạt động trơn tru.
- Để thoát môi trường ảo sau khi code xong, dùng lệnh: `deactivate`
Hướng dẫn cài đặt Project:

    Cài đặt môi trường ảo env:
        python -m venv venv
        venv/Scripts/activate
        
    Cài đặt framework django:
        pip install django

    Cài đặt psycopg2-binary (PostgreSQL):
        pip install psycopg2-binary
    
    Cài đặt restframework:
        python -m pip install djangorestframework

    Cài đặt thư viện Pillow xử lý ảnh:
        pip install Pillow

    Lệnh tạo bảng:
        python manage.py migrate

    Lệnh tạo tài khoản admin:
        python manage.py createsuperuser
        
    Truy cập vào đường link:
        http://127.0.0.1:8000/
    
# Sử dụng image Python chính thức làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Thiết lập biến môi trường để Flask chạy ở chế độ production
ENV FLASK_APP=tiny_app.py
ENV FLASK_ENV=production

# Mở cổng 5000 để ứng dụng Flask chạy
EXPOSE 5000

# Lệnh chạy ứng dụng khi container khởi động
CMD ["flask", "run", "--host=0.0.0.0"]
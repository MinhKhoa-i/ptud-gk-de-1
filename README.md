Vương Nguyễn Minh Khoa - 22681791
# ptud-gk-de-1
## Hướng dẫn cài đặt và chạy
### Cách 1: Chạy ứng dụng trên môi trường local
1. **Clone repo** về máy:
   ```sh
   git clone https://github.com/MinhKhoa-i/ptud-gk-de-1.git
   cd ptud-gk-de-1
   ```
2. **Tạo môi trường ảo và cài đặt thư viện**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Trên macOS/Linux
   venv\Scripts\activate  # Trên Windows
   pip install -r requirements.txt
   ```
3. **Chạy ứng dụng**:
   ```sh
   flask run
   ```
4. **Mở trình duyệt và truy cập**:
   ```
   http://127.0.0.1:5000
   ```

### Cách 2: Chạy ứng dụng bằng Docker
1. **Cài đặt Docker (nếu chưa có)**
2. **Build Docker Image**:
   ```sh
   docker pull vnmkhoa/flask_tiny_app:latest
   ```
3. **Chạy ứng dụng**:
   ```sh
   docker run -p 5000:5000 tiny-app
   ```

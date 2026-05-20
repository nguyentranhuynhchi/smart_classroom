# db_helper.py
import sqlite3
from config import DB_PATH

class DatabaseHelper:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()

    def get_connection(self):
        """Tạo kết nối mới đến SQLite cho mỗi luồng để tránh lỗi xung đột luồng"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Cho phép truy cập dữ liệu theo tên cột
        return conn

    def init_db(self):
        """Khởi tạo cấu trúc bảng dữ liệu lúc ứng dụng khởi động"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Bảng SinhVien lưu trữ thông tin cơ bản và vector đặc trưng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SinhVien (
                mssv TEXT PRIMARY KEY,
                hovaten TEXT NOT NULL,
                lop TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                sdt TEXT UNIQUE,
                face_embedding TEXT,  -- Lưu chuỗi JSON của mảng vector (sẽ làm ở core/face_engine)
                avatar_path TEXT,     -- Đường dẫn vật lý đến ảnh trong dataset_enrollment/
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def check_exists(self, field, value):
        """Kiểm tra xem một giá trị thuộc một cột đã tồn tại trong bảng SinhVien chưa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sử dụng tham số hóa để ngăn chặn lỗi SQL Injection
        query = f"SELECT 1 FROM SinhVien WHERE {field} = ?"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None

    def insert_sinh_vien(self, mssv, hovaten, lop, email, sdt, avatar_path, face_embedding=None):
        """Thực hiện chèn một bản ghi sinh viên mới vào cơ sở dữ liệu"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO SinhVien (mssv, hovaten, lop, email, sdt, avatar_path, face_embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (mssv, hovaten, lop, email, sdt, avatar_path, face_embedding))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Error] Không thể ghi nhận sinh viên vào DB: {e}")
            return False
        finally:
            conn.close()
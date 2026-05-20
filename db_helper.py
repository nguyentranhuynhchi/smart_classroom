# db_helper.py
import sqlite3
from config import DB_PATH

class DatabaseHelper:
    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Khởi tạo cấu trúc bảng dữ liệu bằng tiếng Anh lúc ứng dụng khởi động"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 1. Bảng Student (Quản lý thông tin sinh viên)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Student (
                student_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                class_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE,
                face_embedding TEXT,
                avatar_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Bảng LectureSession (Quản lý các phiên/buổi học)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LectureSession (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. Bảng Attendance (Quản lý trạng thái điểm danh)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                attendance_status TEXT NOT NULL, -- 'Có mặt' hoặc 'Đi trễ'
                FOREIGN KEY (session_id) REFERENCES LectureSession(session_id),
                FOREIGN KEY (student_id) REFERENCES Student(student_id),
                UNIQUE(session_id, student_id) 
            )
        ''')

        # 4. Bảng LearningStatus (Quản lý log hành vi học tập realtime)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LearningStatus (
                status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                learning_behavior TEXT NOT NULL, -- 'Focusing', 'Distracted', 'Sleeping'
                FOREIGN KEY (session_id) REFERENCES LectureSession(session_id),
                FOREIGN KEY (student_id) REFERENCES Student(student_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_new_lecture_session(self, course_name):
        """Khởi tạo một phiên học mới và trả về session_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO LectureSession (course_name) VALUES (?)", (course_name,))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def check_exists(self, field_name, value):
        """Kiểm tra sự tồn tại của trường dữ liệu trong bảng Student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        query = f"SELECT 1 FROM Student WHERE {field_name} = ?"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def insert_student(self, student_id, full_name, class_name, email, phone, avatar_path, face_embedding=None):
        """Thêm mới một tài khoản sinh viên vào cơ sở dữ liệu"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Student (student_id, full_name, class_name, email, phone, avatar_path, face_embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, full_name, class_name, email, phone, avatar_path, face_embedding))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Error] Failed to insert student: {e}")
            return False
        finally:
            conn.close()

    def get_all_valid_embeddings(self):
        """Lấy danh sách tất cả các sinh viên đã được cấu hình Face Vector thành công"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, full_name, face_embedding, avatar_path FROM Student WHERE face_embedding IS NOT NULL")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert_attendance(self, session_id, student_id, attendance_status):
        """Ghi nhận log giao dịch điểm danh của sinh viên"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO Attendance (session_id, student_id, attendance_status)
                VALUES (?, ?, ?)
            ''', (session_id, student_id, attendance_status))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"[Error] Failed to insert attendance: {e}")
            return False
        finally:
            conn.close()

    def insert_learning_status(self, session_id, student_id, learning_behavior):
        """Ghi nhận trạng thái hành vi phân tích từ camera theo định kỳ thời gian"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO LearningStatus (session_id, student_id, learning_behavior)
                VALUES (?, ?, ?)
            ''', (session_id, student_id, learning_behavior))
            conn.commit()
            return True
        except Exception as e:
            print(f"[Error] Failed to insert learning status: {e}")
            return False
        finally:
            conn.close()
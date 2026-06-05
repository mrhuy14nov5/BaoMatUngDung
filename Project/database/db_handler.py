import sqlite3
import os

class DBHandler:
    def __init__(self, db_path="database/ransom_detect.db"):
        # Chuyển đường dẫn tương đối sang đường dẫn tuyệt đối bên trong Project
        if not os.path.isabs(db_path):
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            db_path = os.path.normpath(os.path.join(project_root, db_path))

        # Đảm bảo thư mục database tồn tại
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """Tạo các bảng Logs và Alerts nếu chưa tồn tại theo chuẩn ERD"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT,
                file_path TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT,
                threat_score INTEGER,
                trigger_file TEXT
            )
        ''')
        self.conn.commit()

    def log_event(self, event_type, file_path):
        """Ghi nhận sự kiện File I/O"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Logs (event_type, file_path) VALUES (?, ?)", 
                       (event_type, file_path))
        self.conn.commit()

    def log_alert(self, alert_type, threat_score, trigger_file):
        """Ghi nhận khi phát hiện hành vi giống Ransomware"""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Alerts (alert_type, threat_score, trigger_file) VALUES (?, ?, ?)",
                       (alert_type, threat_score, trigger_file))
        self.conn.commit()
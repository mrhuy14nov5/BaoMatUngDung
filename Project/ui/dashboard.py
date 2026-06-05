import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class DashboardApp:
    def __init__(self, root, db_path="database/ransom_detect.db"):
        self.root = root
        self.root.title("Ransomware Detection Dashboard")
        self.root.geometry("900x600")
        self.db_path = db_path
        
        self.setup_ui()
        self.update_dashboard()

    def setup_ui(self):
        # Chia bố cục màn hình
        self.top_frame = ttk.Frame(self.root, padding="10")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.bottom_frame = ttk.Frame(self.root, padding="10")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Trực quan hóa Biểu đồ bằng Matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.top_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bảng hiển thị danh sách cảnh báo (Alerts)
        ttk.Label(self.bottom_frame, text="Recent Alerts (Danh sách cảnh báo):", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        columns = ("ID", "Time", "Type", "Score", "File")
        self.tree = ttk.Treeview(self.bottom_frame, columns=columns, show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Time", text="Thời gian")
        self.tree.heading("Type", text="Loại cảnh báo")
        self.tree.heading("Score", text="Điểm rủi ro")
        self.tree.heading("File", text="File kích hoạt")
        
        self.tree.column("ID", width=50)
        self.tree.column("Time", width=150)
        self.tree.column("Type", width=150)
        self.tree.column("Score", width=100)
        self.tree.column("File", width=350)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def fetch_data(self):
        """Lấy dữ liệu từ SQLite Database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Lấy số lượng event trong 10 phút gần nhất (nhóm theo phút)
            cursor.execute('''
                SELECT strftime('%M', timestamp) as minute, COUNT(*) 
                FROM Logs 
                WHERE timestamp >= datetime('now', '-10 minutes')
                GROUP BY minute
                ORDER BY timestamp ASC
            ''')
            log_data = cursor.fetchall()
            
            # Lấy danh sách 10 cảnh báo mới nhất
            cursor.execute('SELECT id, timestamp, alert_type, threat_score, trigger_file FROM Alerts ORDER BY id DESC LIMIT 10')
            alerts_data = cursor.fetchall()
            
            conn.close()
            return log_data, alerts_data
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return [], []

    def update_dashboard(self):
        """Cập nhật biểu đồ và bảng dữ liệu mỗi 2 giây"""
        log_data, alerts_data = self.fetch_data()

        # Làm mới dữ liệu biểu đồ 1 (File I/O Events)
        self.ax1.clear()
        if log_data:
            minutes = [row[0] for row in log_data]
            counts = [row[1] for row in log_data]
            self.ax1.plot(minutes, counts, marker='o', color='b')
        self.ax1.set_title("File I/O Events (Last 10 Mins)")
        self.ax1.set_xlabel("Minute")
        self.ax1.set_ylabel("Events Count")

        # Làm mới dữ liệu biểu đồ 2 (Threat Indicator)
        self.ax2.clear()
        current_threat = alerts_data[0][3] if alerts_data else 0
        bars = self.ax2.bar(["Threat Level"], [current_threat], color='red' if current_threat >= 80 else 'green')
        self.ax2.set_ylim(0, 100)
        self.ax2.set_title("Current Max Threat Score")

        self.fig.tight_layout()
        self.canvas.draw()

        # Làm mới danh sách cảnh báo trên TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)
        for alert in alerts_data:
            self.tree.insert("", tk.END, values=alert)

        # Lặp lại việc cập nhật sau 2000ms (2 giây)
        self.root.after(2000, self.update_dashboard)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
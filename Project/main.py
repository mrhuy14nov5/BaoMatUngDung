import os
import time
from detector.engine import DetectionEngine
from detector.monitor import Monitor

# Cấu hình đường dẫn Sandbox an toàn tuyệt đối cho đồ án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SANDBOX_DIR = os.path.join(BASE_DIR, 'sandbox')

def setup_environment():
    """Tạo môi trường Sandbox giả lập và sinh file mẫu để test"""
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
        print(f"[INIT] Đã tạo thư mục sandbox tại: {SANDBOX_DIR}")

        # Sinh file mẫu
        for i in range(5):
            filepath = os.path.join(SANDBOX_DIR, f"document_{i}.txt")
            
            # FIX: thêm encoding utf-8
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Đây là dữ liệu mật của công ty. " * 50)

        print("[INIT] Đã tạo 5 file mẫu để thử nghiệm mã hóa.")
    else:
        print(f"[INIT] Sandbox đã tồn tại: {SANDBOX_DIR}")

def main():
    print("=" * 50)
    print("HỆ THỐNG PHÁT HIỆN RANSOMWARE ")
    print("=" * 50)

    setup_environment()

    # Khởi tạo các Core Module
    engine = DetectionEngine()
    monitor = Monitor(target_dir=SANDBOX_DIR, engine=engine)

    try:
        # Bắt đầu luồng giám sát
        monitor.start()
        print("\n[*] Hệ thống đang chạy ngầm... Bấm Ctrl+C để thoát.")
        print("[*] Gợi ý: Mở terminal mới và chạy 'python simulator/safe_ransomware.py' để test.\n")

        # Vòng lặp giữ chương trình chạy
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[*] Nhận lệnh tắt từ người dùng. Đang dọn dẹp hệ thống...")
        monitor.stop()
        print("[*] Đã tắt thành công.")

if __name__ == "__main__":
    main()
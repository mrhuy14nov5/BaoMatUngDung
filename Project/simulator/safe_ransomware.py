import os
import sys
import time  # Thêm thư viện để làm chậm tốc độ mã hóa
from cryptography.fernet import Fernet

# Cho phép import module khi chạy script trực tiếp từ thư mục gốc
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Đường dẫn sandbox an toàn
SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sandbox'))

class SafeSimulator:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def is_safe_path(self, filepath):
        return os.path.abspath(filepath).startswith(SANDBOX_DIR)

    def simulate_encryption(self):
        print(f"[SIMULATOR] Bắt đầu mã hóa giả lập trong: {SANDBOX_DIR}")
        
        # Tạo 50 file mẫu để có đủ dữ liệu cho Dashboard vẽ biểu đồ
        for i in range(50):
            filepath = os.path.join(SANDBOX_DIR, f"test_data_{i}.txt")
            
            # 1. Tạo file nội dung mẫu
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Đây là dữ liệu cần được bảo vệ và mô phỏng ransomware " * 100)
            
            # 2. Đọc và mã hóa nội dung
            with open(filepath, 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            
            # 3. Ghi đè và đổi tên file
            with open(filepath, 'wb') as f:
                f.write(encrypted_data)
            
            locked_path = filepath + ".locked"
            os.rename(filepath, locked_path)
            
            print(f"  -> Encrypted: test_data_{i}.txt.locked")
            
            # Thêm độ trễ 0.1 giây để hệ thống giám sát kịp ghi nhận từng sự kiện
            # Điều này giúp Dashboard vẽ được đường biểu đồ thay vì chỉ 1 điểm
            time.sleep(0.1) 

if __name__ == "__main__":
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
    
    sim = SafeSimulator()
    sim.simulate_encryption()
    print("[SIMULATOR] Hoàn tất quá trình mô phỏng mã hóa.")
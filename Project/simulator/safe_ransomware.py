import os
from cryptography.fernet import Fernet

# CRITICAL: CHỈ HOẠT ĐỘNG TRONG THƯ MỤC NÀY
SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sandbox'))

class SafeSimulator:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def is_safe_path(self, filepath):
        return os.path.abspath(filepath).startswith(SANDBOX_DIR)

    def simulate_encryption(self):
        print(f"[SIMULATOR] Bắt đầu mã hóa giả lập trong: {SANDBOX_DIR}")
        for root, _, files in os.walk(SANDBOX_DIR):
            for file in files:
                if file.endswith('.txt'): # Chỉ nhắm vào file txt mẫu
                    filepath = os.path.join(root, file)
                    if not self.is_safe_path(filepath):
                        continue
                    
                    # Đọc và mã hóa
                    with open(filepath, 'rb') as f:
                        data = f.read()
                    encrypted_data = self.cipher.encrypt(data)
                    
                    # Ghi đè và đổi tên
                    with open(filepath, 'wb') as f:
                        f.write(encrypted_data)
                    os.rename(filepath, filepath + ".locked")
                    print(f"  -> Encrypted: {filepath}.locked")

if __name__ == "__main__":
    if not os.path.exists(SANDBOX_DIR):
        os.makedirs(SANDBOX_DIR)
        # Tạo file mẫu
        for i in range(5):
            with open(os.path.join(SANDBOX_DIR, f"test_data_{i}.txt"), 'w') as f:
                f.write("Đây là dữ liệu quan trọng " * 100)
    
    sim = SafeSimulator()
    sim.simulate_encryption()
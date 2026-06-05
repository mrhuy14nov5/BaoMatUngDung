import math
import os

def calculate_entropy(file_path, sample_size=10240):
    """Tính toán Shannon Entropy của file (lấy mẫu 10KB để tối ưu tốc độ)"""
    try:
        if not os.path.exists(file_path):
            return 0.0
            
        with open(file_path, 'rb') as f:
            data = f.read(sample_size)
            
        if not data:
            return 0.0
            
        entropy = 0
        # Đếm tần suất các byte (0-255)
        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1
            
        # Tính theo công thức H(X)
        for count in byte_counts:
            if count == 0:
                continue
            p = count / len(data)
            entropy -= p * math.log2(p)
            
        return entropy
    except Exception as e:
        return 0.0
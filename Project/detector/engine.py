import time
from detector.entropy import calculate_entropy
from database.db_handler import DBHandler

class DetectionEngine:
    def __init__(self):
        self.db = DBHandler()
        self.recent_events = [] # [(timestamp, event_type, path)]
        self.threat_score = 0
        self.ENTROPY_THRESHOLD = 7.5

    def analyze_event(self, event_type, path):
        current_time = time.time()
        self.recent_events.append((current_time, event_type, path))
        self.db.log_event(event_type, path)
        
        # Xóa các sự kiện quá 10 giây
        self.recent_events = [e for e in self.recent_events if current_time - e[0] < 10]
        
        self.evaluate_risk(path)

    def evaluate_risk(self, trigger_path):
        self.threat_score = 0
        
        # Rule 1: Mass file activities (> 10 events in 10s)
        if len(self.recent_events) > 10:
            self.threat_score += 40
            
        # Rule 2: High Entropy on modified file
        if self.threat_score > 0 and os.path.exists(trigger_path):
            entropy = calculate_entropy(trigger_path)
            if entropy >= self.ENTROPY_THRESHOLD:
                self.threat_score += 50
                
        # Trigger Alert
        if self.threat_score >= 80:
            print(f"[!!! ALERT !!!] RANSOMWARE BEHAVIOR DETECTED! File: {trigger_path} | Score: {self.threat_score}")
            self.db.log_alert("Ransomware Suspicion", self.threat_score, trigger_path)
            # Trong thực tế: Gọi Windows API để kill process khả nghi tại đây.
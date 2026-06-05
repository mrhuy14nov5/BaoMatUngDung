import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, engine):
        self.engine = engine

    def on_modified(self, event):
        if not event.is_directory:
            self.engine.analyze_event("MODIFIED", event.src_path)

    def on_moved(self, event):
        # Ransomware thường đổi tên phần mở rộng (ví dụ: .txt -> .locked)
        if not event.is_directory:
            self.engine.analyze_event("RENAMED", event.dest_path)

    def on_created(self, event):
        if not event.is_directory:
            self.engine.analyze_event("CREATED", event.src_path)

class Monitor:
    def __init__(self, target_dir, engine):
        self.target_dir = target_dir
        self.engine = engine
        self.observer = Observer()

    def start(self):
        """Bắt đầu tiến trình giám sát thư mục"""
        handler = FileMonitorHandler(self.engine)
        self.observer.schedule(handler, self.target_dir, recursive=True)
        self.observer.start()
        print(f"[*] Đang giám sát thời gian thực thư mục: {self.target_dir}")

    def stop(self):
        """Dừng tiến trình giám sát"""
        self.observer.stop()
        self.observer.join()
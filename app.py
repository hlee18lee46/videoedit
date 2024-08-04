import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from moviepy.editor import VideoFileClip

class VideoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Python Video Editor")
        self.setGeometry(100, 100, 800, 600)
        
        self.openButton = QPushButton("Open Video", self)
        self.openButton.setGeometry(50, 50, 100, 50)
        self.openButton.clicked.connect(self.open_file)
        
        self.saveButton = QPushButton("Save Video", self)
        self.saveButton.setGeometry(200, 50, 100, 50)
        self.saveButton.clicked.connect(self.save_file)
        
        self.trimButton = QPushButton("Trim Video", self)
        self.trimButton.setGeometry(350, 50, 100, 50)
        self.trimButton.clicked.connect(self.trim_video)
        
        self.startLabel = QLabel("Start Time (s):", self)
        self.startLabel.setGeometry(50, 150, 100, 30)
        self.startTime = QLineEdit(self)
        self.startTime.setGeometry(160, 150, 100, 30)
        
        self.endLabel = QLabel("End Time (s):", self)
        self.endLabel.setGeometry(50, 200, 100, 30)
        self.endTime = QLineEdit(self)
        self.endTime.setGeometry(160, 200, 100, 30)
        
        self.video_path = None
        self.save_path = None
    
    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "All Files (*);;Video Files (*.mp4 *.avi)", options=options)
        if file_name:
            self.video_path = file_name
            QMessageBox.information(self, "File Selected", f"Selected file: {file_name}")
    
    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Video File", "", "All Files (*);;Video Files (*.mp4 *.avi)", options=options)
        if file_name:
            self.save_path = file_name
            QMessageBox.information(self, "File Saved", f"Saved as: {file_name}")
    
    def trim_video(self):
        if not self.video_path or not self.save_path:
            QMessageBox.warning(self, "Error", "Please select a video file and save location first.")
            return
        
        try:
            start_time = float(self.startTime.text())
            end_time = float(self.endTime.text())
            
            if start_time >= end_time:
                QMessageBox.warning(self, "Error", "Start time must be less than end time.")
                return
            
            self.perform_trimming(start_time, end_time)
            QMessageBox.information(self, "Success", f"Video trimmed successfully and saved as {self.save_path}")
        
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid start or end time.")
    
    def perform_trimming(self, start_time, end_time):
        video = VideoFileClip(self.video_path).subclip(start_time, end_time)
        video.write_videofile(self.save_path, codec="libx264")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoEditor()
    window.show()
    sys.exit(app.exec_())

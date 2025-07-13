import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from screenshot_ai_agent import ScreenshotAIAgent

class OverlayWindow(QWidget):
    ai_response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.installEventFilter(self)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.92)
        self.is_hidden = False
        self.agent = ScreenshotAIAgent()
        self.screenshot_paths = []
        self.ai_response_signal.connect(self.append_ai_response_mainthread)

    def init_ui(self):
        self.setGeometry(200, 100, 500, 400)
        layout = QVBoxLayout()
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Ask AI about the screenshot...")
        self.input_line.returnPressed.connect(self.handle_prompt)
        clear_btn = QPushButton("Clear (Cmd+R)")
        clear_btn.clicked.connect(self.clear_all)
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(QApplication.instance().quit)
        layout.addWidget(self.chat_area)
        layout.addWidget(self.input_line)
        layout.addWidget(clear_btn)
        layout.addWidget(quit_btn)
        self.setLayout(layout)
        # Set translucent background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255, 220))
        self.setPalette(palette)

    def handle_prompt(self):
        prompt = self.input_line.text().strip()
        if prompt:
            self.chat_area.append(f"You: {prompt}")
            self.input_line.clear()
            self.chat_area.append("AI: (thinking...)")
            threading.Thread(target=self.run_ai_query, args=(prompt,), daemon=True).start()

    def run_ai_query(self, prompt):
        screenshot_path = self.agent.take_screenshot()
        if screenshot_path:
            self.screenshot_paths.append(screenshot_path)
            response = self.agent.query_screenshot(screenshot_path, prompt)
            if response:
                self.ai_response_signal.emit(response)
            else:
                self.ai_response_signal.emit("(Failed to get AI response)")
        else:
            self.ai_response_signal.emit("(Failed to take screenshot)")

    def append_ai_response_mainthread(self, response):
        # Replace last line (AI: (thinking...)) with actual response
        text = self.chat_area.toPlainText().rsplit('\n', 1)[0] + f"\nAI: {response}"
        self.chat_area.setPlainText(text)
        self.chat_area.moveCursor(self.chat_area.textCursor().End)

    def clear_all(self):
        self.chat_area.clear()
        # Remove screenshots taken in this session
        import os
        for path in self.screenshot_paths:
            try:
                os.remove(path)
            except Exception:
                pass
        self.screenshot_paths = []

    def eventFilter(self, obj, event):
        # Cmd+\ to show/hide, Cmd+R to clear
        if event.type() == QEvent.KeyPress:
            if event.modifiers() == Qt.MetaModifier:
                if event.key() == Qt.Key_Backslash:
                    self.toggle_visibility()
                    return True
                elif event.key() == Qt.Key_R:
                    self.clear_all()
                    return True
        return super().eventFilter(obj, event)

    def toggle_visibility(self):
        if self.is_hidden:
            self.show()
            self.is_hidden = False
        else:
            self.hide()
            self.is_hidden = True

def main():
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
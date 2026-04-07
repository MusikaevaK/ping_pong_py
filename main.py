import sys 
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QRectF

WIDTH, HEIGHT = 800, 600

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.keys = set()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logic)
        self.timer.start(16)
        self.paddle_left = QRectF(5, 250, 5, 50)
        self.paddle_right = QRectF(WIDTH - 10, 250, 5, 50)
        self.ball = QRectF(WIDTH/2, HEIGHT/2, 10, 10)
        self.ball_speed_x = 5
        self.ball_speed_y = 5

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor("pink"))

        painter.setBrush(QColor("red"))

        painter.drawRect(self.paddle_left)
        painter.drawRect(self.paddle_right)

        painter.drawEllipse(self.ball)

        painter.setPen(QColor("green"))

        painter.drawLine(int(self.ball.center().x()), 
                         int(self.ball.center().y()), 
                         int (self.ball.center().x() + 5), 
                         int(self.ball.center().y() - 5))
        painter.setPen(Qt.PenStyle.NoPen)

    def keyPressEvent(self, event):
        self.keys.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys:
            self.keys.remove(event.key())

    def update_logic(self):
        self.ball.translate(self.ball_speed_x, self.ball_speed_y)

        if self.ball.top() < 0:
            self.ball.moveTo(WIDTH - self.ball_speed_x, HEIGHT - 1)
        if self.ball.bottom() > HEIGHT:
            self.ball.moveTo(WIDTH - self.ball_speed_x, 0 + 1)
        if self.ball.left() < 0 or self.ball.right() > WIDTH:
            #+рандом
            #+счетчик у противоположного игрока увеличивается
        if self.paddle_left.intersects(self.ball) or self.paddle_right.intersects(self.ball):
            self.ball_speed_x = -self.ball_speed_x 

        if Qt.Key.Key_W in self.keys and self.paddle_left.top() > 4:
            self.paddle_left.translate(0, -5)
        if Qt.Key.Key_S in self.keys and self.paddle_left.bottom() < HEIGHT - 4:
            self.paddle_left.translate(0, 5)
        if Qt.Key.Key_Up in self.keys and self.paddle_right.top() > 4:
            self.paddle_right.translate(0, -5)
        if Qt.Key.Key_Down in self.keys and self.paddle_right.bottom() < HEIGHT - 4:
            self.paddle_right.translate(0, 5)

        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ping pong py")
        self.setFixedSize(WIDTH, HEIGHT)
        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

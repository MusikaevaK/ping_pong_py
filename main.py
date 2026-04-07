import sys 
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt, QTimer, QRectF

WIDTH = 800
HEIGHT = 600
FINAL_SCORE = 21

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
        self.ball_speed_x = random.choice([5, -5])
        self.ball_speed_y = random.choice([5, -5])
        self.score_left_player = 0
        self.score_right_player = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor("pink"))

        painter.setBrush(QColor("red"))

        painter.drawRect(self.paddle_left)
        painter.drawRect(self.paddle_right)

        painter.drawEllipse(self.ball)

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setPen(QColor("green"))

        cx = self.ball.center().x()
        cy = self.ball.center().y() #для движения хвостика относительно движения мяча
        if self.ball_speed_y > 0:
            tail_y = -10
        elif self.ball_speed_y < 0:
            tail_y = 10
        painter.drawLine(int(cx), int(cy), int(cx + 5), int (cy + tail_y))
        
        painter.setPen(Qt.PenStyle.NoPen)

        #painter.drawLine(int(self.ball.center().x()), 
        #                 int(self.ball.center().y()), 
        #                 int (self.ball.center().x() + 5), 
        #                 int(self.ball.center().y() - 5))
        #painter.setPen(Qt.PenStyle.NoPen)

        painter.setPen(QColor("blue"))

        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, f"{self.score_left_player} : {self.score_right_player}")

        painter.setPen(Qt.PenStyle.NoPen)

    def keyPressEvent(self, event):
        self.keys.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys:
            self.keys.remove(event.key())

    def update_logic(self):
        self.ball.translate(self.ball_speed_x, self.ball_speed_y)

        if self.ball.top() < 0:
            self.ball.moveTo(WIDTH - self.ball.x() - self.ball.width(), HEIGHT - self.ball.height() - 5)
            self.ball_speed_x = -self.ball_speed_x
        elif self.ball.bottom() > HEIGHT:
            self.ball.moveTo(WIDTH - self.ball.x() - self.ball.width(), 5)
            self.ball_speed_x = -self.ball_speed_x

        if self.ball.left() < 0 or self.ball.right() > WIDTH:
            if self.ball.left() < 0:
                self.score_right_player += 1 
            else:
                self.score_left_player += 1

            update_x = random.randint(200, 600)
            if random.choice([True, False]):
                update_y = -10 #для плавности захода мяча на поле
                self.ball_speed_y = abs(self.ball_speed_y)
            else:
                update_y = HEIGHT
                self.ball_speed_y = -abs(self.ball_speed_y)

            self.ball.moveTo(update_x, update_y)

            self.ball_speed_x = -5 if self.ball_speed_x > 0 else 5 

        if self.paddle_left.intersects(self.ball) or self.paddle_right.intersects(self.ball):
            self.ball_speed_x = -self.ball_speed_x 
            self.ball_speed_x *= 1.05

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

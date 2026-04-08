import sys 
import random
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer, QRectF, QPoint, QRect

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
        self.timer.start(16) #60 fps

        self.paddle_left = QRectF(5, 250, 5, 50)
        self.paddle_right = QRectF(WIDTH - 10, 250, 5, 50)
        self.ball = QRectF(WIDTH/2, HEIGHT/2, 20, 20)
        self.ball_speed_x = random.choice([5, -5])
        self.ball_speed_y = random.choice([5, -5])
        self.cherry_img = QPixmap("cherry.png")
        self.cherry_tail_img = QPixmap("cherry_tail.png")
        self.cherry_leaves_img = QPixmap("cherry_leaves.png")
        self.score_left_player = 0
        self.score_right_player = 0
        self.run_game = True
        self.left_player_win = False
        self.right_player_win = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("pink"))

        painter.setBrush(QColor("red"))
        painter.drawRect(self.paddle_left)
        painter.drawRect(self.paddle_right)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawPixmap(self.ball.toRect(), self.cherry_img)
        cx = self.ball.toRect().center().x()
        cy = self.ball.toRect().center().y() 
        
        tail_size = 10
        tail_offset_y = -10 
        tail_rect = QRect(0, 0, tail_size, tail_size)
        tail_rect.moveCenter(QPoint(cx - 1, cy + tail_offset_y)) #сx - 2 тк в файле хвостик под наклоном 
        painter.drawPixmap(tail_rect, self.cherry_tail_img)

        leaves_size = 10
        leaves_offset_y = -10 
        leaves_rect = QRect(0, 0, leaves_size, leaves_size)
        leaves_rect.moveCenter(QPoint(cx - 3, cy + leaves_offset_y))
        painter.drawPixmap(leaves_rect, self.cherry_leaves_img)
        
        #painter.drawLine(int(cx), int(cy), int(cx + 5), int (cy + tail_y))
    
        #painter.drawLine(int(self.ball.center().x()), 
        #                 int(self.ball.center().y()), 
        #                 int (self.ball.center().x() + 5), 
        #                 int(self.ball.center().y() - 5))

        painter.setPen(QColor("blue"))
        if self.run_game:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, f"{self.score_left_player} : {self.score_right_player}")
        else:
            overlay_color = QColor(255, 255, 255, 50) #??
            painter.fillRect(self.rect(), overlay_color)
            winner = "ТОТ, ЧТО СЛЕВА <-" if self.left_player_win else "ТОТ, ЧТО СПРАВА ->"
            font = painter.font()
            font.setPointSize(20)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"ПОБЕДИЛ {winner}\nМОЖЕШЬ ВЗЯТЬ ПОСЛЕДНЮЮ ВИШЕНКУ.")

        painter.setPen(Qt.PenStyle.NoPen)

    def keyPressEvent(self, event):
        self.keys.add(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keys:
            self.keys.remove(event.key())

    def update_logic(self):
        if not self.run_game:
            return 

        if Qt.Key.Key_W in self.keys and self.paddle_left.top() > 4:
            self.paddle_left.translate(0, -5)
        if Qt.Key.Key_S in self.keys and self.paddle_left.bottom() < HEIGHT - 4:
            self.paddle_left.translate(0, 5)
        if Qt.Key.Key_Up in self.keys and self.paddle_right.top() > 4:
            self.paddle_right.translate(0, -5)
        if Qt.Key.Key_Down in self.keys and self.paddle_right.bottom() < HEIGHT - 4:
            self.paddle_right.translate(0, 5)

        self.ball.translate(self.ball_speed_x, self.ball_speed_y)

        if self.ball.top() < 0:
            self.ball.moveTop(0)
            self.ball_speed_y = -self.ball_speed_y
        elif self.ball.bottom() > HEIGHT:
            self.ball.moveBottom(HEIGHT)
            self.ball_speed_y = -self.ball_speed_y

        if self.ball.left() < 0 or self.ball.right() > WIDTH:
            if self.ball.left() < 0:
                self.score_right_player += 1 
                if self.score_right_player == FINAL_SCORE:
                    self.run_game = False
                    self.right_player_win = True
                    self.timer.stop()
            else:
                self.score_left_player += 1
                if self.score_left_player == FINAL_SCORE:
                    self.run_game = False
                    self.left_player_win = True
                    self.timer.stop()

            #update_x = random.randint(200, 600)
            #if random.choice([True, False]):
                #update_y = -self.ball.height() - 5 #для плавности захода мяча на поле
                #self.ball_speed_y = abs(self.ball_speed_y)
            #else:
                #update_y = HEIGHT + 5
                #self.ball_speed_y = -abs(self.ball_speed_y)
            
            self.ball_speed_x = random.choice([self.ball_speed_x, -self.ball_speed_x])
            self.ball.moveTo(WIDTH/2, HEIGHT/2)

            #self.ball_speed_x = -self.ball_speed_x if self.ball_speed_x > 0 else self.ball_speed_x 

        if self.paddle_left.intersects(self.ball) or self.paddle_right.intersects(self.ball):
            if self.ball_speed_x < 0:
                self.score_left_player += 1
                self.ball.moveLeft(self.paddle_left.right())
            else:
                self.score_right_player += 1
                self.ball.moveRight(self.paddle_right.left())

            self.ball_speed_x = -self.ball_speed_x 
            self.ball_speed_x *= 1.05

            if abs(self.ball_speed_y) > 5:
                self.ball_speed_y = 5 if self.ball_speed_y > 0 else -5

        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("cherry pong")
        self.setFixedSize(WIDTH, HEIGHT)
        self.game_widget = GameWidget()
        self.setCentralWidget(self.game_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
